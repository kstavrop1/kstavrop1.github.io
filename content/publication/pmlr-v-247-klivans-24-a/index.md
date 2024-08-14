---
title: Testable Learning with Distribution Shift
date: '2024-06-28'
draft: false
publishDate: '2024-08-12T19:48:58.161640Z'
authors:
- Adam Klivans
- admin
- Arsen Vasilyan
publication_types:
- 'paper-conference'
abstract: '  We revisit the fundamental problem of learning with distribution shift,
  in which a learner is given labeled samples from training distribution $D$, unlabeled
  samples from test distribution $D{’}$ and is asked to output a classifier with low test
  error.  The standard approach in this setting is to bound the loss of a classifier
  in terms of some notion of distance between $D$ and $D{’}$.  These distances, however,
  seem difficult to compute and do not lead to efficient algorithms. We depart from
  this paradigm and define a new model called  testable learning with distribution
  shift, where we can obtain provably efficient algorithms for certifying the performance
  of a classifier on a test distribution.  In this model, a learner outputs a classifier
  with low test error whenever samples from $D$ and $D{’}$ pass an associated test; moreover,
  the test must accept (with high probability) if the marginal of $D$ equals the marginal
  of $D{’}$. We give several positive results for learning well-studied concept classes
  such as halfspaces, intersections of halfspaces, and decision trees when the marginal
  of $D$ is Gaussian or uniform on the hypercube.  Prior to our work, no efficient algorithms
  for these basic cases were known without strong assumptions on $D{’}$. For halfspaces
  in the realizable case (where there exists a halfspace consistent with both $D$ and
  $D{’}$), we combine a moment-matching approach with ideas from active learning to simulate
  an efficient oracle for estimating disagreement regions. To extend to the non-realizable
  setting, we apply recent work from testable (agnostic) learning.  More generally,
  we prove that any function class with low-degree $\mathcal{L_2}$-sandwiching polynomial
  approximators can be learned in our model.  Since we require $\mathcal{L_2}$- sandwiching
  (instead of the usual $\mathcal{L_1}$ loss), we cannot directly appeal to convex duality
  and instead apply constructions from the pseudorandomness literature to obtain the
  required approximators.  We also provide lower bounds to show that the guarantees
  we obtain on the performance of our output hypotheses are best possible up to constant
  factors, as well as a separation showing that realizable learning in our model is
  incomparable to (ordinary) agnostic learning.'
featured: true
publication: '*Proceedings of Thirty Seventh Conference on Learning Theory*'
url_pdf: https://proceedings.mlr.press/v247/klivans24a/klivans24a.pdf
links:
- name: URL
  url: https://proceedings.mlr.press/v247/klivans24a.html
---

