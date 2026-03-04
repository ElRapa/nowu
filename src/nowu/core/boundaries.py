"""Import boundary policy for nowu modules.

Used by architecture tests to prevent unplanned coupling.
"""

ALLOWED_INTERNAL_IMPORTS: dict[str, set[str]] = {
    "core": set(),
    "flow": {"core"},
    "bridge": {"core", "flow"},
    "soul": set(),
}
