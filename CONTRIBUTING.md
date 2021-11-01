# Contributing Guidelines

Thank you for investing your time in contributing to our project!

There are two main ways to contribute to the project - submitting issues and submitting
fixes/changes/improvements via pull requests.

## Submitting issues

Both bug reports and feature requests are welcome.
Submit issues [here](https://github.com/NOWUM/EnSysMod/issues).

* Search for existing issues to avoid reporting duplicates.
* When submitting a bug report:
  * Test it against the most recently released version. It might have been already fixed.
  * Include the code that reproduces the problem or attach the link to the repository with the project which fully reproduces the problem.
  * However, don't put off reporting any weird or rarely appearing issues just because you cannot consistently reproduce them.
  * If the bug is in behavior, then explain what behavior you've expected and what you've got.
* When submitting a feature request:
  * Explain why you need the feature - what's your use-case, what's your domain.
  * Explaining the problem you face is more important than suggesting a solution.
    Report your problem even if you don't have any proposed solution.
  * If there is an alternative way to do what you need, then show the code of the alternative.

## Submitting PRs

We love PRs. Submit PRs [here](https://github.com/NOWUM/EnSysMod/pulls) after reading the [PR Workflow](#pr-workflow).
However, please keep in mind that maintainers will have to support the resulting code of the project,
so do familiarize yourself with the following guidelines.

* All development (both new features and bug fixes) is performed in the `main` branch.
  * Base PRs against the `main` branch.
  * PR should be linked with the issue, excluding minor documentation changes, the addition of unit tests, and fixing typos.
* If you make any code changes:
  * Follow the [Python Coding Conventions](https://www.python.org/dev/peps/pep-0008/).
  * [Build the project](#building) to make sure it all works and passes the tests.
* If you fix a bug:
  * Write the test the reproduces the bug.
  * Fixes without tests are accepted only in exceptional circumstances if it can be shown that writing the corresponding test is too hard or otherwise impractical.
  * Follow the style of writing tests that is used in this project: name test classes as `xxx_test.py`.
* If you introduce any new public APIs:
  * All new APIs must come with documentation and tests.
  * If you plan API additions, then please start by submitting an issue with the proposed API design to gather community feedback.
  * [Contact the maintainers](#contacting-maintainers) to coordinate any big piece of work in advance via submitting an issue.
* If you fix documentation:
  * If you plan extensive rewrites/additions to the docs, then please [contact the maintainers](#contacting-maintainers) to coordinate the work in advance.


## How to fix an existing issue

* If you are going to work on the existing issue:
  * Comment on the existing issue if you want to work on it. 
  * Wait till it is assigned to you by [maintainers](#contacting-maintainers). 
  * Ensure that the issue not only describes a problem, but also describes a solution that had received a positive feedback. Propose a solution if there isn't any.
* If you are going to submit your first PR in this project:
  * Find tickets with the label ["good first issue"](https://github.com/NOWUM/EnSysMod/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22+no%3Aassignee) 
    which are not assigned to somebody.
  * Learn the [`examples`](https://github.com/NOWUM/EnSysMod/tree/main/examples) module, submit new interesting example or improve documentation for one of them.
* If you are an experienced developer with good knowledge of Keras/TensorFlow/PyTorch/ONNX framework, find tickets with the label
  ["good second issue"](https://github.com/NOWUM/EnSysMod/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+second+issue%22+no%3Aassignee),
  which are not assigned to somebody.
* If you are ready to participate in library design and in new experiments, find tickets with the label
  ["research"](https://github.com/NOWUM/EnSysMod/issues?q=is%3Aissue+is%3Aopen+label%3Aresearch).
  
  
## Development workflow
1. Checkout the project using Git.
   - New to Git? Get Git [here](https://git-scm.com/downloads)!
   - Clone project `git clone https://github.com/NOWUM/EnSysMod.git`
   - Navigate into project folder `cd EnSysMod`
2. Install all pre requirements for development
   - New to Python? Get Python [here](https://www.python.org/downloads/)!
   - Create environment `sh scripts/install.sh`
3. Check if project is fine
   - Run tests `sh scripts/test.sh`
4. Open the project in an IDE of your choice
   - You like [PyCharm](https://www.jetbrains.com/pycharm/)? See [this](https://www.jetbrains.com/help/pycharm/open-projects.html) guide.
   - You like [VSCode](https://code.visualstudio.com/)? See [this](https://code.visualstudio.com/docs/python/python-tutorial) guide.
5. Time to code! Develop your changes
   - Run main `sh scripts/run.sh`
   - Run tests `sh scripts/test.sh`
   - Run linting `sh scripts/lint.sh`
7. Ready? Commit your changes
   - Create a new Branch `git checkout -b <branch-name>` <br>The Branch should be named like `feature/user-guide` or `fix/background-color`.
   - Check changed files `git status`
   - Add changed files `git add <file-name>` or all of them using `git add .`
   - Commit your changes `git commit -m "<your message>"` <br>The Message should describe your changes like `Added development workflow guide` or `Updated development workflow guide`. See [this](https://www.freecodecamp.org/news/writing-good-commit-messages-a-practical-guide/) guide for more information.
   - Push your changes `git push`
8. All finished? Checkout the [PR workflow](#pr-workflow)


## PR workflow

0. Contributor build the project locally and run all unit tests and integration tests. (If it's possible on contributor machine...) 
1. Contributor submits the PR if the local build is successful and tests are green.
2. Reviewer marks the PR with the "Review" label at the start of the review process.
3. Reviewer leaves the comments or marks the PR with the label "LGTM."
4. Contributor answers the comments or fixes the proposed PR.
5. Reviewer marks the PR with the label "LGTM."
6. Maintainer could suggest merging the `main` branch to the PR branch a few times due to changes in the `main` branch.
7. Maintainer runs TC builds (unit tests and examples as integration tests).
8. The TC writes the result (passed or not passed) to the PR checks at the bottom of the proposed PR.
9. If it is possible, maintainers share the details of the failed build with the contributor.
10. Maintainer merges the PR if all checks are successful and there is no conflict with the master branch.


## Release workflow [Maintainer only]
0. This task is only for Maintainers!
1. Merge all PRs into `main` that should be part of next release.
2. Run `sh scripts/release.sh [major|minor|patch]` locally.
3. Check the PR created for your release [here](https://github.com/NOWUM/EnSysMod/pulls?q=is%3Apr+is%3Aopen+label%3Arelease).
4. Check if documentation is still up-to-date. You can push changes to branch `release/x.x.x`.
5. Merge PR if everything looks good to you.
6. Wait CI/CD for creating your release. See the new release [here](https://github.com/NOWUM/EnSysMod/releases/latest).
7. Edit the release and click on button `+ Auto-generate release notes`.
8. 🎉 Done! 🎉

## Contacting maintainers

* If something cannot be done, not convenient, or does not work - submit an [issue](#submitting-issues).
* To attract attention to the problem or raised question or a new comment, mention @v3lop5.
