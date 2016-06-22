Project Design
==============

Summary
-------

A weighted attribute matrix is a way of making a choice between
several options with many competiting criteria. It could be useful in
any of the following citeria:

  * What house should we buy? This involves lots of criteria such as
    price, location, size, local facilities etc.
  * What country should I move to? Critera include distance, availability of work,
    politics, climate, language etc.

A weighted attribute matrix is comprised of the following:

Options
:   These are the options you are trying to decide between. In the case of
    moving country these could be: USA, United Kingom, France, Australia.

Criteria
:   A way of assessing the options. In the case of
    moving country these could relate to: politics, climate, language etc.

Weights
:   A numerical value which indicates the importance of a given option.
    For example, you may not care much about politics, but you care a lot
    about climate. Often values of 0 (don't care) to 5 (mandatory) will be used.

Scores
:   A numerical value which indicates how well an option (i.e. Australia)
    satisfies a given criteria (i.e. climate). Often values of 0
    (does not satisfy at all) to 5 (completely satisfies) will be used.

Categories
:   Groups of criteria which can be useful for creating a high-level
    summary of how each option has scored.

Entities
--------

Core:

 * Option
 * Criteria
 * Weight
 * Score
 * Category

Additional:

 * Score labels - ability to give a specified criteria custom score labels
   (e.g: Weather: 0 - miserable, 1 - grey, 2 - chilly summer, 3 - warm summer,
   4 - hot summer, 5 - year-round hot/warm)
 * Allow multiple people to score & weight, then offer comparisons.
   * Link each weight to the given user
   * Link each score to the given user

Interfaces
----------

  * Criteria management (incl weighting, category selection)
  * Option management
  * Category management
  * Scoring
  * Report
