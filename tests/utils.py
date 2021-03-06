import inspect
from typing import (Any,
                    Callable,
                    Iterable,
                    Hashable,
                    Dict,
                    List)

from hypothesis import (Verbosity,
                        find,
                        settings)
from hypothesis.searchstrategy import SearchStrategy


def example(strategy: SearchStrategy) -> Any:
    return find(specifier=strategy,
                condition=lambda x: True,
                settings=settings(max_shrinks=0,
                                  max_iterations=10000,
                                  database=None,
                                  verbosity=Verbosity.quiet))


def double_star_map(function: Callable[..., Any],
                    kwargs: Dict[str, Any]) -> Any:
    return function(**kwargs)


def initializer_parameters(cls: type) -> List[str]:
    initializer_signature = inspect.signature(cls.__init__)
    parameters = dict(initializer_signature.parameters)
    parameters.pop('self')
    return list(parameters.keys())


def sub_dict(dictionary: Dict[Hashable, Any],
             *,
             keys: Iterable[Hashable]) -> Dict[Hashable, Any]:
    return {key: dictionary[key]
            for key in keys}
