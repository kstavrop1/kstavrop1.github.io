---
title: 'Sparse Linear Regression is Easy on Random Supports'
date: '2026-01-02'
draft: false
publishDate: ''
authors:
- Gautam Chandrasekaran
- Raghu Meka
- admin
publication_types:
- 'paper-conference'
abstract: 'Sparse linear regression is one of the most basic questions in machine learning and statistics. Here, we are given as input a design matrix $\bf{X} \in \mathbb{R}^{N \times d}$ and measurements or labels $\bf{y} \in \mathbb{R}^N$ where $\bf{y} = \bf{X} \bf{w}^* +  \xi$, and $ \xi$ is the noise in the measurements. Importantly, we have the additional constraint that the unknown signal vector $\bf{w}^* $ is sparse: it has $k$ non-zero entries where $k$ is much smaller than the ambient dimension. Our goal is to output a prediction vector $\widehat{\bf{w}}$ that has small prediction error: $\frac{1}{N}\cdot \|\bf{X} \bf{w}^* - \bf{X} \widehat{\bf{w}}\|^2_2$. 

Information-theoretically, we know what is best possible in terms of measurements: under most natural noise distributions, we can get  prediction error at most $\epsilon$ with roughly $N = O(k \log d/\epsilon)$ samples. Computationally, this currently needs $d^{\Omega(k)}$ run-time. Alternately, with $N = O(d)$, we can get polynomial-time. Thus, there is an exponential gap (in the dependence on $d$) between the two and we do not know if it is possible to get $d^{o(k)}$ run-time and $o(d)$ samples. 

We give the first generic positive result for worst-case design matrices $\bf{X}$: For any $\bf{X}$, we show that if the support of $\bf{w}^* $ is chosen at random, we can get prediction error $\epsilon$ with  $N = \mathrm{poly}(k, \log d, 1/\epsilon)$ samples and run-time $\mathrm{poly}(d,N)$. This run-time holds for any design matrix $\bf{X}$ with condition number up to $2^{\mathrm{poly}(d)}$. 

Previously, such results were known for worst-case $\bf{w}^*$, but only for random design matrices from well-behaved families, matrices that have a very low condition number ($\mathrm{poly}(\log d)$; e.g., as studied in compressed sensing), or those with special structural properties. '
featured: true
publication: '**STOC 2026**'
url_pdf: 'https://arxiv.org/pdf/2511.06211'
links:
 - name: URL
   url: 'https://arxiv.org/abs/2511.06211'
---