"""
Error recovery and retry logic for the Deep Research Workflow System.

Provides:
- Exponential backoff retry logic
- Error categorization and handling
- Escalation thresholds
- Recovery strategies
"""

import asyncio
import logging
from typing import Callable, Optional, Any, TypeVar
from enum import Enum

logger = logging.getLogger("error_recovery")

T = TypeVar("T")


class ErrorSeverity(Enum):
    """Categorizes error severity levels."""

    RECOVERABLE = "recoverable"  # Can retry
    DEGRADED = "degraded"  # Continue with reduced functionality
    CRITICAL = "critical"  # Cannot continue


class ErrorCategory(Enum):
    """Categorizes error types."""

    API_ERROR = "api_error"  # External API failures
    NETWORK_ERROR = "network_error"  # Network connectivity issues
    TIMEOUT_ERROR = "timeout_error"  # Operation timeouts
    VALIDATION_ERROR = "validation_error"  # Input validation failures
    RESOURCE_ERROR = "resource_error"  # Resource (memory, disk) issues
    UNKNOWN_ERROR = "unknown_error"  # Unclassified errors


def categorize_error(error: Exception) -> ErrorCategory:
    """
    Categorize an exception into known error types.

    Args:
        error: The exception to categorize

    Returns:
        ErrorCategory classification
    """
    error_str = str(error).lower()

    if "timeout" in error_str or isinstance(error, asyncio.TimeoutError):
        return ErrorCategory.TIMEOUT_ERROR

    if "api" in error_str or "401" in error_str or "403" in error_str:
        return ErrorCategory.API_ERROR

    if "network" in error_str or "connection" in error_str:
        return ErrorCategory.NETWORK_ERROR

    if "validation" in error_str or "invalid" in error_str:
        return ErrorCategory.VALIDATION_ERROR

    if "memory" in error_str or "disk" in error_str:
        return ErrorCategory.RESOURCE_ERROR

    return ErrorCategory.UNKNOWN_ERROR


def get_error_severity(error: Exception) -> ErrorSeverity:
    """
    Determine severity of an error.

    Args:
        error: The exception to evaluate

    Returns:
        ErrorSeverity level
    """
    category = categorize_error(error)

    if category == ErrorCategory.VALIDATION_ERROR:
        return ErrorSeverity.CRITICAL  # Don't retry invalid input

    if category == ErrorCategory.RESOURCE_ERROR:
        return ErrorSeverity.CRITICAL  # Can't continue without resources

    if category in [
        ErrorCategory.API_ERROR,
        ErrorCategory.TIMEOUT_ERROR,
    ]:
        return ErrorSeverity.RECOVERABLE  # Can retry

    if category == ErrorCategory.NETWORK_ERROR:
        return ErrorSeverity.RECOVERABLE  # Network issues may be temporary

    return ErrorSeverity.DEGRADED


async def retry_with_backoff(
    func: Callable[..., Any],
    *args,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    **kwargs,
) -> Any:
    """
    Execute an async function with exponential backoff retry logic.

    Args:
        func: Async function to execute
        *args: Positional arguments for func
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay between retries (seconds)
        max_delay: Maximum delay between retries (seconds)
        exponential_base: Base for exponential backoff calculation
        **kwargs: Keyword arguments for func

    Returns:
        Result from successful function execution

    Raises:
        Exception: Final exception if all retries fail
    """
    last_exception = None
    delay = initial_delay

    for attempt in range(max_retries + 1):
        try:
            logger.info(
                f"Attempt {attempt + 1}/{max_retries + 1} to execute {func.__name__}"
            )
            result = await func(*args, **kwargs)
            logger.info(f"{func.__name__} succeeded on attempt {attempt + 1}")
            return result

        except Exception as e:
            last_exception = e
            severity = get_error_severity(e)
            category = categorize_error(e)

            logger.warning(
                f"{func.__name__} failed (attempt {attempt + 1}): "
                f"{category.value} - {str(e)} (severity: {severity.value})"
            )

            # Don't retry critical errors
            if severity == ErrorSeverity.CRITICAL:
                logger.error(f"Critical error in {func.__name__}: {str(e)}")
                raise

            # Last attempt failed
            if attempt == max_retries:
                logger.error(
                    f"{func.__name__} failed after {max_retries + 1} attempts"
                )
                raise

            # Wait before retrying
            await asyncio.sleep(delay)
            delay = min(delay * exponential_base, max_delay)

    # Should never reach here
    raise last_exception


async def with_fallback(
    primary: Callable[..., Any],
    fallback: Callable[..., Any],
    *args,
    **kwargs,
) -> Any:
    """
    Execute primary function, fall back to secondary on failure.

    Args:
        primary: Primary async function to execute
        fallback: Fallback async function if primary fails
        *args: Arguments for both functions
        **kwargs: Keyword arguments for both functions

    Returns:
        Result from successful function execution

    Raises:
        Exception: If both primary and fallback fail
    """
    try:
        logger.info(f"Attempting primary: {primary.__name__}")
        result = await primary(*args, **kwargs)
        logger.info(f"Primary succeeded: {primary.__name__}")
        return result

    except Exception as e:
        logger.warning(
            f"Primary failed ({primary.__name__}): {str(e)}. "
            f"Attempting fallback ({fallback.__name__})"
        )

        try:
            result = await fallback(*args, **kwargs)
            logger.info(f"Fallback succeeded: {fallback.__name__}")
            return result

        except Exception as fallback_error:
            logger.error(
                f"Both primary and fallback failed. "
                f"Primary: {str(e)}, Fallback: {str(fallback_error)}"
            )
            raise RuntimeError(
                f"Both primary and fallback operations failed. "
                f"Primary: {str(e)}, Fallback: {str(fallback_error)}"
            )


def should_escalate(error_count: int, max_iterations: int) -> bool:
    """
    Determine if error threshold requires escalation to user.

    Args:
        error_count: Number of errors encountered
        max_iterations: Maximum allowed iterations

    Returns:
        True if should escalate to user
    """
    # Escalate if we've reached max iterations
    return error_count >= max_iterations


class ResilientOperation:
    """
    Wraps an async operation with error handling and recovery.

    Usage:
        operation = ResilientOperation(my_async_func)
        result = await operation.execute(arg1, arg2, kwarg1=value1)
    """

    def __init__(
        self,
        func: Callable,
        max_retries: int = 3,
        timeout: Optional[float] = None,
    ):
        """
        Initialize resilient operation wrapper.

        Args:
            func: Async function to wrap
            max_retries: Maximum number of retries
            timeout: Operation timeout in seconds
        """
        self.func = func
        self.max_retries = max_retries
        self.timeout = timeout
        self.attempt_count = 0
        self.error_history = []

    async def execute(self, *args, **kwargs) -> Any:
        """
        Execute the wrapped function with error handling.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result

        Raises:
            Exception: If all retries fail
        """
        try:
            if self.timeout:
                return await asyncio.wait_for(
                    self.func(*args, **kwargs),
                    timeout=self.timeout,
                )
            else:
                return await self.func(*args, **kwargs)

        except asyncio.TimeoutError as e:
            self.error_history.append(("timeout", str(e)))
            logger.error(f"{self.func.__name__} timed out after {self.timeout}s")
            raise

        except Exception as e:
            self.error_history.append((categorize_error(e).value, str(e)))
            logger.error(f"{self.func.__name__} failed: {str(e)}")
            raise

    async def execute_with_retry(self, *args, **kwargs) -> Any:
        """
        Execute with automatic retry logic.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result
        """
        return await retry_with_backoff(
            self.func,
            *args,
            max_retries=self.max_retries,
            **kwargs,
        )


# Error recovery strategies

async def partial_recovery(
    items: list,
    processor: Callable,
    fail_on_count: Optional[int] = None,
) -> tuple[list, list]:
    """
    Process items with partial failure recovery.

    Args:
        items: Items to process
        processor: Async function to process each item
        fail_on_count: Max allowed failures before stopping

    Returns:
        Tuple of (successful_results, failed_items)
    """
    successful = []
    failed = []

    for i, item in enumerate(items):
        try:
            result = await processor(item)
            successful.append(result)

        except Exception as e:
            logger.warning(f"Failed to process item {i}: {str(e)}")
            failed.append({"item": item, "error": str(e)})

            # Stop if too many failures
            if fail_on_count and len(failed) >= fail_on_count:
                logger.error(f"Stopping after {fail_on_count} failures")
                break

    logger.info(
        f"Processed {len(successful)} items successfully, "
        f"{len(failed)} failed"
    )

    return successful, failed
