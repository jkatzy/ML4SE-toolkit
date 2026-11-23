# Implementing a paper-backed module

Use this workflow to add or change a published method anywhere under `src/ml4setk/`.
Identify the owning source module and its public API before choosing the relevant
package guide. For membership-inference methods, see the
[MIA guide](../../docs/membership_inference.md).

1. **Identify the method and its baselines.** Verify the conference or journal
   version with the publisher. Record the title, all authors in publication
   order, venue, year, and DOI or proceedings URL. Give each baseline its own
   module entry and credit both its originators and the study evaluating it.
   Link an existing entry when a later paper uses the same baseline.
2. **Establish provenance.** Follow the authors' artifact link. Pin a version
   DOI or commit and identify the files relevant to the contribution. If the
   authors released no artifact, record the sources checked and what evidence
   will be used for verification.
3. **Decide what may ship.** Record whether the contribution is original code,
   a port, a dependency, or redistributed material. Check the paper, code,
   datasets, and fixtures separately. Compare the applicable terms with both
   the toolkit license file and its distribution metadata. For third-party
   material record the copyright holder, license, compatibility reasoning,
   required notices and their shipping location. When rights are unclear,
   leave that material out and document what evidence would resolve the issue.
4. **Define and test the contribution.** Specify which part of the paper the
   API covers, its inputs, conventions, output, and any deviations. Put the
   method citation in its module docstring and user documentation. Add
   deterministic tests for the conventions most likely to change results.
   Keep large reference artifacts external and optional imports local.
5. Deliver the reusable method under `src/ml4setk/` with a public entry point
   that accepts the documented inputs and returns the method's result. Keep
   benchmark setup and paper comparisons in the reproduction script. Run a
   minimal example against the installed package and document the invocation
   and observed output.
6. Publish the citation and reuse record beside the example in the module guide.
   Run the focused tests, `make lint`, and `make smoke`. Use the shared
   [reproduction workflow](reproduction.md) to check the published experiments.
