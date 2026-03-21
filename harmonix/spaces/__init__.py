"""
harmonix.spaces
======================
Built-in domain-specific search spaces.

All types are importable directly from this sub-package **or** from the
top-level ``harmonix`` namespace.

Mathematical spaces
-------------------
.. code-block:: python

    from harmonix.spaces import (
        NaturalNumber, WholeNumber,
        NegativeInt, NegativeReal, PositiveReal,
        PrimeVariable, PowerOfTwo, Fibonacci,
    )

Engineering spaces
------------------
.. code-block:: python

    from harmonix.spaces import ACIRebar, ACIDoubleRebar

Registry names
--------------
Every type is also accessible via the plugin registry:

.. code-block:: python

    from harmonix import create_variable
    var = create_variable("prime", hi=100)
    var = create_variable("aci_rebar", d_expr=0.55, cc_expr=40.0)
"""

from .engineering import (
    ACIDoubleRebar,
    ACIRebar,
    ConcreteGrade,
    ConcreteGradeProperties,
    SectionProperties,
    SeismicZone,
    SeismicZoneTBDY,
    SoilProfile,
    SoilSPT,
    SteelSection,
)
from .math import (
    Fibonacci,
    NaturalNumber,
    NegativeInt,
    NegativeReal,
    PositiveReal,
    PowerOfTwo,
    PrimeVariable,
    WholeNumber,
)

__all__ = [
    # math
    "NaturalNumber",
    "WholeNumber",
    "NegativeInt",
    "NegativeReal",
    "PositiveReal",
    "PrimeVariable",
    "PowerOfTwo",
    "Fibonacci",
    # engineering — rebar
    "ACIRebar",
    "ACIDoubleRebar",
    # engineering — sections & materials
    "SteelSection",
    "SectionProperties",
    "ConcreteGrade",
    "ConcreteGradeProperties",
    # engineering — geotechnical
    "SoilSPT",
    "SoilProfile",
    # engineering — seismic
    "SeismicZoneTBDY",
    "SeismicZone",
]
