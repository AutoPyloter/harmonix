"""
registry.py
===========
Plugin registry and ``make_variable`` factory for custom search spaces.

Three ways to define a custom variable
---------------------------------------

**1. Subclass** (full control, recommended for complex domains):

.. code-block:: python

    from hsds import Variable, register_variable

    @register_variable("rebar_aci")
    class ACIRebarVariable(Variable):
        def sample(self, ctx): ...
        def filter(self, candidates, ctx): ...
        def neighbor(self, value, ctx): ...

**2. Factory function** (quick prototyping, no class boilerplate):

.. code-block:: python

    from hsds import make_variable

    PrimeVar = make_variable(
        name="prime",
        sample=lambda ctx: random.choice(PRIMES),
        filter=lambda cands, ctx: [c for c in cands if c in PRIME_SET],
        neighbor=lambda val, ctx: next_prime(val),
    )
    space.add("p", PrimeVar(lo=2, hi=100))

**3. Registry lookup** (use a previously registered type by name):

.. code-block:: python

    from hsds import create_variable

    var = create_variable("rebar_aci", d_expr=0.55, cc_expr=40.0)

Design notes
------------
* Names are case-insensitive, normalised to lower-case.
* Built-in types (continuous, discrete, integer, categorical) and all
  types from ``hsds.spaces`` are pre-registered at import time.
* Re-registering an existing name raises ``VariableAlreadyRegisteredError``
  unless ``overwrite=True``.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional, Type

from .variables import Categorical, Continuous, Discrete, Integer, Variable

# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class VariableNotFoundError(KeyError):
    """Raised when a variable type name is not in the registry."""


class VariableAlreadyRegisteredError(KeyError):
    """Raised when a name is registered a second time without overwrite."""


# ---------------------------------------------------------------------------
# Internal store
# ---------------------------------------------------------------------------

_REGISTRY: Dict[str, Type[Variable]] = {}


def _normalise(name: str) -> str:
    return name.strip().lower()


# ---------------------------------------------------------------------------
# register_variable
# ---------------------------------------------------------------------------


def register_variable(
    name: str,
    cls: Optional[Type[Variable]] = None,
    *,
    overwrite: bool = False,
):
    """
    Register a :class:`Variable` subclass under *name*.

    Usable as a decorator or a plain function call.

    Parameters
    ----------
    name : str
        Lookup key (case-insensitive).
    cls : type, optional
        Class to register.  Omit when using as a decorator.
    overwrite : bool
        Allow replacing an existing registration.
    """
    key = _normalise(name)

    def _register(klass: Type[Variable]) -> Type[Variable]:
        if not (isinstance(klass, type) and issubclass(klass, Variable)):
            raise TypeError(f"Only Variable subclasses can be registered; got {klass!r}.")
        if key in _REGISTRY and not overwrite:
            raise VariableAlreadyRegisteredError(f"'{name}' is already registered. Pass overwrite=True to replace.")
        _REGISTRY[key] = klass
        return klass

    return _register(cls) if cls is not None else _register


# ---------------------------------------------------------------------------
# make_variable
# ---------------------------------------------------------------------------


def make_variable(
    sample: Callable,
    filter: Callable,  # noqa: A002
    neighbor: Callable,
    *,
    name: Optional[str] = None,
    register: bool = False,
) -> Type[Variable]:
    """
    Create a :class:`Variable` subclass from three plain functions.

    This is a convenience factory for quick prototyping.  The resulting
    class behaves identically to a hand-written subclass.

    Parameters
    ----------
    sample : callable
        ``sample(ctx) -> value``
    filter : callable
        ``filter(candidates, ctx) -> List[value]``
    neighbor : callable
        ``neighbor(value, ctx) -> value``
    name : str, optional
        Class name (used in ``repr`` and registry).  Defaults to
        ``"CustomVariable"``.
    register : bool
        If ``True`` and *name* is given, register the class automatically.

    Returns
    -------
    type
        A new :class:`Variable` subclass (the class itself, not an instance).
        Instantiate it normally: ``var = MyVar()``.

    Examples
    --------
    >>> import random
    >>> PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    >>> PrimeVar = make_variable(
    ...     sample   = lambda ctx: random.choice(PRIMES),
    ...     filter   = lambda cands, ctx: [c for c in cands if c in PRIMES],
    ...     neighbor = lambda val, ctx: PRIMES[
    ...         max(0, min(len(PRIMES)-1, PRIMES.index(val) + random.choice([-1,1])))
    ...         if val in PRIMES else 0
    ...     ],
    ...     name="prime",
    ... )
    >>> space.add("p", PrimeVar())
    """
    class_name = name or "CustomVariable"

    _sample_fn = sample
    _filter_fn = filter
    _neighbor_fn = neighbor

    class _CustomVariable(Variable):
        def sample(self, ctx):
            return _sample_fn(ctx)

        def filter(self, candidates, ctx):  # noqa: A003
            return _filter_fn(candidates, ctx)

        def neighbor(self, value, ctx):
            return _neighbor_fn(value, ctx)

    _CustomVariable.__name__ = class_name
    _CustomVariable.__qualname__ = class_name

    if register and name:
        register_variable(name, _CustomVariable)

    return _CustomVariable


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------


def get_variable_class(name: str) -> Type[Variable]:
    """
    Return the class registered under *name*.

    Raises :class:`VariableNotFoundError` if not found.
    """
    key = _normalise(name)
    try:
        return _REGISTRY[key]
    except KeyError:
        raise VariableNotFoundError(
            f"No variable type '{name}' in registry. Available: {list_variable_types()}"
        ) from None


def create_variable(name: str, *args, **kwargs) -> Variable:
    """
    Instantiate the variable type registered under *name*.

    Positional and keyword arguments are forwarded to the constructor.
    """
    return get_variable_class(name)(*args, **kwargs)


def list_variable_types() -> List[str]:
    """Return sorted list of all registered variable type names."""
    return sorted(_REGISTRY.keys())


def unregister_variable(name: str) -> None:
    """
    Remove *name* from the registry.

    Raises :class:`VariableNotFoundError` if not found.
    """
    key = _normalise(name)
    if key not in _REGISTRY:
        raise VariableNotFoundError(f"Cannot unregister '{name}': not found.")
    del _REGISTRY[key]


# ---------------------------------------------------------------------------
# Pre-register built-in primitive types
# ---------------------------------------------------------------------------

register_variable("continuous", Continuous, overwrite=True)
register_variable("discrete", Discrete, overwrite=True)
register_variable("integer", Integer, overwrite=True)
register_variable("categorical", Categorical, overwrite=True)
