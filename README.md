# NATMS
An negation assumption based truth maintenance system (ATMS)

NATMS presents itself as a natural evolution of basic ATMS without the use of Hyperresolution rules. With the possibility to represent and process assumptions like A<sub>1</sub>, A<sub>2</sub>, A<sub>n</sub> indicated as *choose*{A<sub>1</sub>, A<sub>2</sub>, A<sub>n</sub>} which are complicated for simple ATMS without Hyperresolution rules. NATMS has the algorithm structure and input data that remain almost unchanged and handles these cases effectively and efficiently as done in classic ATMS. NATMS allows the presence of denied assumptions directly within the antecedents of the justifications. This allows NATMS to immediately represent *choose*{A, B, C} in &not;A, &not;B, &not;C justification 

The NATMS is based exactly on this notation, which is very expressive in fact, if we wanted to represent it in the ATMS it is necessary to include these three implications.\
A &and; B &rarr; &not;C\
A &and; C &rarr; &not;B\
B &and; C &rarr; &not;A\
Implications that we find encoded within the nodes of our data structure in case we process the rule within NATMS.

The algorithm is taking from *Johan De Kleer. A general labeling algorithm for assumption-based truth maintenance. InAAAI, volume 88, pages188–192, 198* and is implemented in Python. 
Compared to the algorithm indicated, however, it has been modified the third point that you are going to add in the NOGOOD function. In fact, instead of searching within the *antecendents* of the NoGood node justifications, if &not;A is named, as indicated, it was necessary to perform the search for A. This change was made because without it the examples given did not give the same results.

In addition to this substantial modification, two other refinements have been made that solve some problems during the tests.

The first one modifies is the &not; A node creation when running the NOGOOD function when we have A inside the environment. Since in some examples, as a result, we had the symbol &perp;, which we remember means *False*, inside an environment and the creation of the node &not; &perp;, this initialization has been completely removed and as expected this generation did not occur again.

The other change is suggested inside the paper in section 8 useful because for some problems you can solve the problem of the lack of completeness of the label inside the NATMS exposed in section 7.
The change involves a detail of representation of the denied assumptions that are not considered assumptions but simple nodes, as you can read in section 5 when presenting NATMS, this difference affects the initial state of the node object. The assumptions have as environment themselves, which in the ATMS cannot be valid since in the environment only the assumptions can appear.
To solve this problem it has been necessary to consider also the denied assumptions &not;A this allows that such propositions are present inside the environment and go to solve cases like this

A &rarr; b , &not; A &rarr; b

in which we will have as a result the node b with a single environment {A} when in reality it should also be present {$\neg A$}, so the label is therefore not complete.
This change solves this problem without affecting the performance and the results of the previous changes.