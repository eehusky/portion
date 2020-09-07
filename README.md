# portion - data structure and operations for intervals

[![Travis](https://travis-ci.org/AlexandreDecan/portion.svg?branch=master)](https://travis-ci.org/AlexandreDecan/portion)
[![Coverage Status](https://coveralls.io/repos/github/AlexandreDecan/portion/badge.svg?branch=master)](https://coveralls.io/github/AlexandreDecan/portion?branch=master)
[![License](https://badgen.net/pypi/license/portion)](https://github.com/AlexandreDecan/portion/blob/master/LICENSE.txt)
[![PyPI](https://badgen.net/pypi/v/portion)](https://pypi.org/project/portion)
[![Commits](https://badgen.net/github/last-commit/AlexandreDecan/portion)](https://github.com/AlexandreDecan/portion/commits/)

This fork of AlexandreDecan portions library only supports floating point operations with the ability to do fuzzy comparisons on interval values.

The `portion` library (formerly distributed as `python-intervals`) provides data structure and operations for intervals in Python 3.5+.

 - Support intervals of any (comparable) objects.
 - Closed or open, finite or (semi-)infinite intervals.
 - Interval sets (union of atomic intervals) are supported.
 - Automatic simplification of intervals.
 - Support comparison, transformation, intersection, union, complement, difference and containment.
 - Provide test for emptiness, atomicity, overlap and adjacency.
 - Discrete iterations on the values of an interval.
 - Dict-like structure to map intervals to data.
 - Import and export intervals to strings and to Python built-in data types.
 - Heavily tested with high code coverage.

**Latest release:**
 - `portion`: 2.1.1 on 2020-08-21 ([documentation](https://github.com/AlexandreDecan/portion/blob/2.1.1/README.md), [changes](https://github.com/AlexandreDecan/portion/blob/2.1.1/CHANGELOG.md)).
 - `python-intervals`: 1.10.0 on 2019-09-26 ([documentation](https://github.com/AlexandreDecan/portion/blob/1.10.0/README.md), [changes](https://github.com/AlexandreDecan/portion/blob/1.10.0/README.md#changelog)).

 Note that `python-intervals` will no longer receive updates since it has been replaced by `portion`.


## Table of contents

  * [Installation](#installation)
  * [Documentation & usage](#documentation--usage)
      * [Interval creation](#interval-creation)
      * [Interval bounds & attributes](#interval-bounds--attributes)
      * [Interval operations](#interval-operations)
      * [Comparison operators](#comparison-operators)
      * [Interval transformation](#interval-transformation)
      * [Discrete iteration](#discrete-iteration)
      * [Map intervals to data](#map-intervals-to-data)
      * [Import & export intervals to strings](#import--export-intervals-to-strings)
      * [Import & export intervals to Python built-in data types](#import--export-intervals-to-python-built-in-data-types)
  * [Changelog](#changelog)
  * [Contributions](#contributions)
  * [License](#license)


## Installation

You can use `pip` to install it, as usual: `pip install portion`.

This will install the latest available version from [PyPI](https://pypi.org/project/portion).
Pre-releases are available from the *master* branch on [GitHub](https://github.com/AlexandreDecan/portion)
and can be installed with `pip install git+https://github.com/AlexandreDecan/portion`.

The test environment can be installed with `pip install portion[test]` and relies on [pytest](https://docs.pytest.org/en/latest/).

`portion` is also available on [conda-forge](https://anaconda.org/conda-forge/portion).


## Documentation & usage

### Interval creation

Assuming this library is imported using `import portion as P`, intervals can be easily
created using one of the following helpers:

```python
>>> P.open(1, 2)
(1,2)
>>> P.closed(1, 2)
[1,2]
>>> P.openclosed(1, 2)
(1,2]
>>> P.closedopen(1, 2)
[1,2)
>>> P.singleton(1)
[1]
>>> P.empty()
()

```

The bounds of an interval can be any arbitrary values, as long as they are comparable:

```python
>>> P.closed(1.2, 2.4)
[1.2,2.4]
>>> P.closed('a', 'z')
['a','z']
>>> import datetime
>>> P.closed(datetime.date(2011, 3, 15), datetime.date(2013, 10, 10))
[datetime.date(2011, 3, 15),datetime.date(2013, 10, 10)]

```


Infinite and semi-infinite intervals are supported using `P.inf` and `-P.inf` as upper or lower bounds.
These two objects support comparison with any other object.
When infinities are used as a lower or upper bound, the corresponding boundary is automatically converted to an open one.

```python
>>> P.inf > 'a', P.inf > 0, P.inf > True
(True, True, True)
>>> P.openclosed(-P.inf, 0)
(-inf,0]
>>> P.closed(-P.inf, P.inf)  # Automatically converted to an open interval
(-inf,inf)

```

Empty intervals always resolve to `(P.inf, -P.inf)`, regardless of the provided bounds:

```python
>>> P.empty() == P.open(P.inf, -P.inf)
True
>>> P.closed(4, 3) == P.open(P.inf, -P.inf)
True
>>> P.openclosed('a', 'a') == P.open(P.inf, -P.inf)
True

```

Intervals created with this library are `Interval` instances.
An `Interval` instance is a disjunction of atomic intervals each representing a single interval (e.g. `[1,2]`).
Intervals can be iterated to access the underlying atomic intervals, sorted by their lower and upper bounds.

```python
>>> list(P.open(10, 11) | P.closed(0, 1) | P.closed(20, 21))
[[0,1], (10,11), [20,21]]

```

Atomic intervals can also be retrieved by position:

```python
>>> (P.open(10, 11) | P.closed(0, 1) | P.closed(20, 21))[0]
[0,1]
>>> (P.open(10, 11) | P.closed(0, 1) | P.closed(20, 21))[-2]
(10,11)

```

For convenience, intervals are automatically simplified:

```python
>>> P.closed(0, 2) | P.closed(2, 4)
[0,4]
>>> P.closed(1, 2) | P.closed(3, 4) | P.closed(2, 3)
[1,4]
>>> P.empty() | P.closed(0, 1)
[0,1]
>>> P.closed(1, 2) | P.closed(2, 3) | P.closed(4, 5)
[1,3] | [4,5]

```

Note that discrete intervals are **not** supported by `portion` (but they can be simulated though, see [#24](https://github.com/AlexandreDecan/portion/issues/24#issuecomment-604456362)).
For example, combining `[0,1]` with `[2,3]` will **not** result in `[0,3]` even if there is
no integer between `1` and `2`.



[&uparrow; back to top](#table-of-contents)
### Interval bounds & attributes


An `Interval` defines the following properties:

 - `i.empty` is `True` if and only if the interval is empty.
   ```python
   >>> P.closed(0, 1).empty
   False
   >>> P.closed(0, 0).empty
   False
   >>> P.openclosed(0, 0).empty
   True
   >>> P.empty().empty
   True

   ```

 - `i.atomic` is `True` if and only if the interval is a disjunction of a single (possibly empty) interval.
   ```python
   >>> P.closed(0, 2).atomic
   True
   >>> (P.closed(0, 1) | P.closed(1, 2)).atomic
   True
   >>> (P.closed(0, 1) | P.closed(2, 3)).atomic
   False

   ```

 - `i.enclosure` refers to the smallest atomic interval that includes the current one.
   ```python
   >>> (P.closed(0, 1) | P.open(2, 3)).enclosure
   [0,3)

   ```

The left and right boundaries, and the lower and upper bounds of an interval can be respectively accessed
with its `left`, `right`, `lower` and `upper` attributes.
The `left` and `right` bounds are either `P.CLOSED` or `P.OPEN`.
By definition, `P.CLOSED == ~P.OPEN` and vice-versa.

```python
>> P.CLOSED, P.OPEN
CLOSED, OPEN
>>> x = P.closedopen(0, 1)
>>> x.left, x.lower, x.upper, x.right
(CLOSED, 0, 1, OPEN)

```

If the interval is not atomic, then `left` and `lower` refer to the lower bound of its enclosure,
while `right` and `upper` refer to the upper bound of its enclosure:

```python
>>> x = P.open(0, 1) | P.closed(3, 4)
>>> x.left, x.lower, x.upper, x.right
(OPEN, 0, 4, CLOSED)

```

One can easily check for some interval properties based on the bounds of an interval:

```python
>>> x = P.openclosed(-P.inf, 0)
>>> # Check that interval is left/right closed
>>> x.left == P.CLOSED, x.right == P.CLOSED
(False, True)
>>> # Check that interval is left/right bounded
>>> x.lower == -P.inf, x.upper == P.inf
(True, False)
>>> # Check for singleton
>>> x.lower == x.upper
False

```



[&uparrow; back to top](#table-of-contents)
### Interval operations

`Interval` instances support the following operations:

 - `i.intersection(other)` and `i & other` return the intersection of two intervals.
   ```python
   >>> P.closed(0, 2) & P.closed(1, 3)
   [1,2]
   >>> P.closed(0, 4) & P.open(2, 3)
   (2,3)
   >>> P.closed(0, 2) & P.closed(2, 3)
   [2]
   >>> P.closed(0, 2) & P.closed(3, 4)
   ()

   ```

 - `i.union(other)` and `i | other` return the union of two intervals.
   ```python
   >>> P.closed(0, 1) | P.closed(1, 2)
   [0,2]
   >>> P.closed(0, 1) | P.closed(2, 3)
   [0,1] | [2,3]

   ```

 - `i.complement(other)` and `~i` return the complement of the interval.
   ```python
   >>> ~P.closed(0, 1)
   (-inf,0) | (1,inf)
   >>> ~(P.open(-P.inf, 0) | P.open(1, P.inf))
   [0,1]
   >>> ~P.open(-P.inf, P.inf)
   ()

   ```

 - `i.difference(other)` and `i - other` return the difference between `i` and `other`.
   ```python
   >>> P.closed(0,2) - P.closed(1,2)
   [0,1)
   >>> P.closed(0, 4) - P.closed(1, 2)
   [0,1) | (2,4]

   ```

 - `i.contains(other)` and `other in i` hold if given item is contained in the interval.
 It supports intervals and arbitrary comparable values.
   ```python
   >>> 2 in P.closed(0, 2)
   True
   >>> 2 in P.open(0, 2)
   False
   >>> P.open(0, 1) in P.closed(0, 2)
   True

   ```

 - `i.adjacent(other)` tests if the two intervals are adjacent.
 Two intervals are adjacent if their intersection is empty, and their union is an atomic interval.
   ```python
   >>> P.closed(0, 1).adjacent(P.openclosed(1, 2))
   True
   >>> P.closed(0, 1).adjacent(P.closed(1, 2))
   False
   >>> (P.closed(0, 1) | P.closed(2, 3)).adjacent(P.open(1, 2) | P.open(3, 4))
   True
   >>> P.closed(0, 1).adjacent(P.open(1, 2) | P.open(10, 11))
   False

   ```

 - `i.overlaps(other)` tests if there is an overlap between two intervals.
   ```python
   >>> P.closed(1, 2).overlaps(P.closed(2, 3))
   True
   >>> P.closed(1, 2).overlaps(P.open(2, 3))
   False

   ```



[&uparrow; back to top](#table-of-contents)
### Comparison operators

Equality between intervals can be checked with the classical `==` operator:

```python
>>> P.closed(0, 2) == P.closed(0, 1) | P.closed(1, 2)
True
>>> P.closed(0, 2) == P.open(0, 2)
False

```

Moreover, intervals are comparable using e.g. `>`, `>=`, `<` or `<=`.
These comparison operators have a different behaviour than the usual ones.
For instance, `a < b` holds if `a` is entirely on the left of the lower bound of `b` and `a > b` holds if `a` is entirely
on the right of the upper bound of `b`.

```python
>>> P.closed(0, 1) < P.closed(2, 3)
True
>>> P.closed(0, 1) < P.closed(1, 2)
False

```

Similarly, `a <= b` holds if `a` is entirely on the left of the upper bound of `b`, and `a >= b`
holds if `a` is entirely on the right of the lower bound of `b`.

```python
>>> P.closed(0, 1) <= P.closed(2, 3)
True
>>> P.closed(0, 2) <= P.closed(1, 3)
True
>>> P.closed(0, 3) <= P.closed(1, 2)
False

```

Intervals can also be compared with single values. If `i` is an interval and `x` a value, then
`x < i` holds if `x` is on the left of the lower bound of `i` and `x <= i` holds if `x` is on the
left of the upper bound of `i`.

```python
>>> 5 < P.closed(0, 10)
False
>>> 5 <= P.closed(0, 10)
True
>>> P.closed(0, 10) < 5
False
>>> P.closed(0, 10) <= 5
True

```

This behaviour is similar to the one that could be obtained by first converting `x` to a
singleton interval (except for infinities since they resolve to empty intervals).

Note that all these semantics differ from classical comparison operators.
As a consequence, some intervals are never comparable in the classical sense, as illustrated hereafter:

```python
>>> P.closed(0, 4) <= P.closed(1, 2) or P.closed(0, 4) >= P.closed(1, 2)
False
>>> P.closed(0, 4) < P.closed(1, 2) or P.closed(0, 4) > P.closed(1, 2)
False
>>> P.empty() < P.empty()
True
>>> P.empty() < P.closed(0, 1) and P.empty() > P.closed(0, 1)
True

```

Finally, intervals are hashable as long as their bounds are hashable (and we have defined a hash value for `P.inf` and `-P.inf`).



[&uparrow; back to top](#table-of-contents)
### Interval transformation

Intervals are immutable but provide a `replace` method to create a new interval based on the
current one. This method accepts four optional parameters `left`, `lower`, `upper`, and `right`:

```python
>>> i = P.closed(0, 2)
>>> i.replace(P.OPEN, -1, 3, P.CLOSED)
(-1,3]
>>> i.replace(lower=1, right=P.OPEN)
[1,2)

```

Functions can be passed instead of values. If a function is passed, it is called with the current corresponding
value except if the corresponding bound is an infinity and parameter `ignore_inf` if set to `False`.

```python
>>> P.closed(0, 2).replace(upper=lambda x: 2 * x)
[0,4]
>>> i = P.closedopen(0, P.inf)
>>> i.replace(upper=lambda x: 10)  # No change, infinity is ignored
[0,inf)
>>> i.replace(upper=lambda x: 10, ignore_inf=False)  # Infinity is not ignored
[0,10)

```

When `replace` is applied on an interval that is not atomic, it is extended and/or restricted such that
its enclosure satisfies the new bounds.

```python
>>> i = P.openclosed(0, 1) | P.closed(5, 10)
>>> i.replace(P.CLOSED, -1, 8, P.OPEN)
[-1,1] | [5,8)
>>> i.replace(lower=4)
(4,10]

```

To apply an arbitrary transformation on an interval, intervals expose an `apply` method.
This method accepts a function that will be applied on each of the underlying atomic intervals to perform the desired transformation.
The function is expected to return either an `Interval`, or a 4-uple `(left, lower, upper, right)`.

```python
>>> i = P.closed(2, 3) | P.open(4, 5)
>>> # Increment bound values
>>> i.apply(lambda x: (x.left, x.lower + 1, x.upper + 1, x.right))
[3,4] | (5,6)
>>> # Invert bounds
>>> i.apply(lambda x: (~x.left, x.lower, x.upper, ~x.right))
(2,3) | [4,5]

```

The `apply` method is very powerful when used in combination with `replace`.
Because the latter allows functions to be passed as parameters and can ignore infinities, it can be
conveniently used to transform intervals in presence of infinities.

```python
>>> i = P.openclosed(-P.inf, 0) | P.closed(3, 4) | P.closedopen(8, P.inf)
>>> # Increment bound values
>>> i.apply(lambda x: x.replace(upper=lambda v: v + 1))
(-inf,1] | [3,5] | [8,inf)
>>> # Intervals are still automatically simplified
>>> i.apply(lambda x: x.replace(lower=lambda v: v * 2))
(-inf,0] | [16,inf)
>>> # Invert bounds
>>> i.apply(lambda x: x.replace(left=lambda v: ~v, right=lambda v: ~v))
(-inf,0) | (3,4) | (8,inf)
>>> # Replace infinities with -10 and 10
>>> conv = lambda v: -10 if v == -P.inf else (10 if v == P.inf else v)
>>> i.apply(lambda x: x.replace(lower=conv, upper=conv, ignore_inf=False))
(-10,0] | [3,4] | [8,10)

```


[&uparrow; back to top](#table-of-contents)
### Discrete iteration

The `iterate` function takes an interval, and returns a generator to iterate over
the values of an interval. Obviously, as intervals are continuous, it is required to specify the
 `step` between consecutive values. The iteration then starts from the lower bound and ends on the upper one,
given they are not excluded by the interval:

```python
>>> list(P.iterate(P.closed(0, 3), step=1))
[0, 1, 2, 3]
>>> list(P.iterate(P.closed(0, 3), step=2))
[0, 2]
>>> list(P.iterate(P.open(0, 3), step=2))
[2]

```

When an interval is not atomic, `iterate` consecutively iterates on all underlying atomic
intervals, starting from each lower bound and ending on each upper one:

```python
>>> list(P.iterate(P.singleton(0) | P.singleton(3) | P.singleton(5), step=2))  # Won't be [0]
[0, 3, 5]
>>> list(P.iterate(P.closed(0, 2) | P.closed(4, 6), step=3))  # Won't be [0, 6]
[0, 4]

```

By default, the iteration always starts on the lower bound of each underlying atomic interval.
The `base` parameter can be used to change this behaviour, by specifying how the initial value to start
the iteration from must be computed. This parameter accepts a callable that is called with the lower
bound of each underlying atomic interval, and that returns the initial value to start the iteration from.
It can be helpful to deal with (semi-)infinite intervals, or to *align* the generated values of the iterator:

```python
>>> # Align on integers
>>> list(P.iterate(P.closed(0.3, 4.9), step=1, base=int))
[1, 2, 3, 4]
>>> # Restrict values of a (semi-)infinite interval
>>> list(P.iterate(P.openclosed(-P.inf, 2), step=1, base=lambda x: max(0, x)))
[0, 1, 2]

```

The `base` parameter can be used to change how `iterate` applies on unions of atomic interval, by
specifying a function that returns a single value, as illustrated next:

```python
>>> base = lambda x: 0
>>> list(P.iterate(P.singleton(0) | P.singleton(3) | P.singleton(5), step=2, base=base))
[0]
>>> list(P.iterate(P.closed(0, 2) | P.closed(4, 6), step=3, base=base))
[0, 6]

```

Notice that defining `base` such that it returns a single value can be extremely inefficient in
terms of performance when the intervals are "far apart" each other (i.e., when the *gaps* between
atomic intervals are large).

Finally, iteration can be performed in reverse order by specifying `reverse=True`.

```python
>>> list(P.iterate(P.closed(0, 3), step=-1, reverse=True))  # Mind step=-1
[3, 2, 1, 0]
>>> list(P.iterate(P.closed(0, 3), step=-2, reverse=True))  # Mind step=-2
[3, 1]

```
