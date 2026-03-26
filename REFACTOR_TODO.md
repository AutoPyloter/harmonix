# Refactor Progress: harmonix → hsds

## Tasks
- [x] Search for all instances of harmonix/harmonix-opt/harmonix_opt/Harmonix
- [x] Update all Python files (core library)
- [x] Update documentation files (README.md, etc.)
- [x] Update configuration files (pyproject.toml, etc.)
- [x] Update GitHub workflow files
- [x] Update benchmark documentation
- [x] Convert British English to American English
- [x] Rename files/folders containing "harmonix"

## Files Modified

### Configuration Files
- **pyproject.toml**: Updated project URLs from harmonix to hsds, fixed British English "optimisation" → "optimization" in keywords
- **sonar-project.properties**: Updated sonar.projectKey from AutoPyloter_harmonix to AutoPyloter_hsds, sonar.projectName from harmonix to hsds, sonar.sources from harmonix to hsds
- **ruff.toml**: Updated comment and per-file-ignores paths from harmonix to hsds
- **mypy.ini**: Updated mypy section headers from harmonix to hsds
- **CITATION.cff**: Updated title from "harmonix-opt: Harmony Search optimisation" to "HSDS: Harmony Search Optimization", URLs from harmonix to hsds, version to 1.0.2
- **.vscode/settings.json**: Updated sonarlint projectKey from AutoPyloter_harmonix to AutoPyloter_hsds

### GitHub Workflows
- **.github/workflows/ci.yml**: Updated ruff check, mypy, and pytest coverage paths from harmonix to hsds
- **.github/workflows/tests.yml**: Updated pytest coverage path from harmonix to hsds
- **.github/workflows/sonarcloud.yml**: Updated pytest coverage path from harmonix to hsds
- **.github/workflows/publish.yml**: Updated package verification grep from harmonix_opt to hsds, PyPI URL from harmonix-opt to hsds

### Documentation Files
- **README.md**: Already updated (no changes needed)
- **BENCHMARK_REPORT.md**: Updated "The Harmonix Benchmark Suite" → "The HSDS Benchmark Suite", "The Harmonix Advantage" → "The HSDS Advantage", all references to "Harmonix library" → "HSDS library"
- **STATISTICAL_REPORT.md**: Updated "the Harmonix library's" → "the HSDS library's"
- **benchmarks/METHODOLOGY.md**: Updated "Harmonix Benchmark Methodology" → "HSDS Benchmark Methodology", "Harmonix Benchmark Suite" → "HSDS Benchmark Suite", "Harmonix completely eliminates" → "HSDS completely eliminates"
- **benchmarks/spring_design/ANALYSIS.md**: Updated "the Harmonix optimizer" → "the HSDS optimizer"
- **benchmarks/speed_reducer/ANALYSIS.md**: Updated "the Harmonix library" → "the HSDS library"
- **benchmarks/retaining_wall/ANALYSIS.md**: Updated "Harmonix ACIRebar" → "HSDS ACIRebar"

### Core Library (Python)
- **hsds/__init__.py**: Fixed British English "optimisation" → "optimization" in module docstring
- **hsds/optimizer.py**: Updated "optimisation" → "optimization", "minimised" → "minimized", "minimiser" → "minimizer"
- **hsds/logging.py**: Updated "optimisation" → "optimization"
- **hsds/pareto.py**: Updated "minimised" → "minimized", "maximised" → "maximized"

### Test Files
- **tests/test_logging.py**: Updated "behaviour" → "behavior"
- **tests/test_bandwidth.py**: Updated "behaviour" → "behavior"
- **tests/test_variables.py**: Updated "behaviour" → "behavior"
- **tests/test_spaces.py**: Updated "behaviour" → "behavior"

### Example Files
- **examples/01_quickstart.py**: Updated "minimise" → "minimize"
- **examples/04_custom_variable.py**: Updated "minimises" → "minimizes", "minimise" → "minimize"
- **examples/05_multi_objective.py**: Updated "optimisation" → "optimization"
- **examples/07_rc_section_full.py**: Updated "optimisation" → "optimization"

### Benchmark Utilities
- **benchmarks/utils/plotter.py**: Updated "colour" → "color"

## Remaining References (Not Changed)
The following files contain "harmonix" references but were intentionally not changed:
- **changes.diff**: Historical diff file showing previous changes
- **.mypy_cache/**: Auto-generated cache files (will regenerate)
- **pytest_out.txt**: Auto-generated test output (will regenerate)
- **.hypothesis/**: Auto-generated test database (will regenerate)

## Summary
All user-facing and source code files have been updated from "harmonix" to "hsds" and all British English spellings have been converted to American English. The library is now consistently named "HSDS" (Harmony Search in Dependent Space) throughout the codebase.
