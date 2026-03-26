"""
space.py
========
DesignSpace — ordered container of named design variables.

The space preserves insertion order (Python 3.7+ dict guarantee) so that
dependency contexts are always built in the correct sequential order:
variable *k* only sees values of variables defined *before* it.
"""

from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional, Tuple

from .variables import Variable


class DesignSpace:
    """
    Ordered mapping from variable names to :class:`~variables.Variable` objects.

    Parameters
    ----------
    variables : dict[str, Variable], optional
        Initial set of variables.  Order is preserved.

    Examples
    --------
    >>> from hsds import DesignSpace, Continuous, Discrete
    >>> space = DesignSpace()
    >>> space.add("h",  Continuous(0.3, 1.2))
    >>> space.add("bf", Continuous(lo=lambda ctx: ctx["h"], hi=0.6))
    >>> space.add("n",  Discrete(4, 1, 20))
    """

    def __init__(self, variables: Optional[Dict[str, Variable]] = None):
        self._vars: Dict[str, Variable] = {}
        if variables:
            for name, var in variables.items():
                self.add(name, var)

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def add(self, name: str, variable: Variable) -> "DesignSpace":
        """Add a named variable.  Returns *self* for chaining."""
        if not isinstance(variable, Variable):
            raise TypeError(f"Expected a Variable instance for '{name}', got {type(variable).__name__}.")
        self._vars[name] = variable
        return self

    def __setitem__(self, name: str, variable: Variable) -> None:
        self.add(name, variable)

    def __getitem__(self, name: str) -> Variable:
        return self._vars[name]

    def __contains__(self, name: str) -> bool:
        return name in self._vars

    def __iter__(self) -> Iterator[str]:
        return iter(self._vars)

    def __len__(self) -> int:
        return len(self._vars)

    def __repr__(self) -> str:
        names = list(self._vars.keys())
        return f"DesignSpace({names})"

    def names(self) -> List[str]:
        """Return variable names in definition order."""
        return list(self._vars.keys())

    def items(self) -> Iterator[Tuple[str, Variable]]:
        """Iterate over (name, variable) pairs in definition order."""
        return iter(self._vars.items())

    # ------------------------------------------------------------------
    # Sampling
    # ------------------------------------------------------------------

    def sample_harmony(self) -> Dict[str, Any]:
        """
        Draw a complete harmony by sampling each variable in order.

        Each variable receives the context built so far, so dependent
        variable bounds resolve correctly.
        """
        harmony: Dict[str, Any] = {}
        for name, var in self._vars.items():
            harmony[name] = var.sample(ctx=harmony)
        return harmony
