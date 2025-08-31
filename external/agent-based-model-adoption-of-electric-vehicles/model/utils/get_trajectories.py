from typing import Dict, List, Tuple, Type

from multiprocess import Pool
from pandas import DataFrame
from tqdm import tqdm

from ..constants import CV, EV, PHEV
from ..Society import Society


def get_trajectories(
    society_class: Type[Society],
    society_kwargs,
    T: int,
    MC: int,
    threads: int = 1,
) -> Tuple[List[DataFrame], List[DataFrame], List[DataFrame], DataFrame]:
    """Function count MC trajectories for seted society_class and
        society_kwargs and time horizont T.
        Function runs in parallel on the set number of threads.

    Args:
        society_class (Type[Society]): Society class for run simulations
        society_kwargs (Dict[str, Any]): Deflaut kwargs for Society.
        T (int): for single simulation
        MC (int): MC repetitions.
        threads (int, optional): Threads to use in multithreads run. Defaults to 1.

    Raises:
        AttributeError: Error raised if threads are not positive int.

    Returns:
        Tuple[List[DataFrame], List[DataFrame], List[DataFrame], DataFrame]:
            Tuple of list results. CVs, EVs, PHEVs, years.
    """
    if threads == 1:
        ret = _get_trajectories_one_thread(society_class, society_kwargs, T, MC)
    elif threads == int(threads) and threads > 0:
        ret = _get_trajectories_multi_threads(
            society_class, society_kwargs, T, MC, threads
        )
    else:
        raise AttributeError(f"threads must be positive integer, not {threads}")
    CVs = [df[CV] for df in ret]
    EVs = [df[EV] for df in ret]
    PHEVs = [df[PHEV] for df in ret]
    year = ret[0]["year"]
    return (CVs, EVs, PHEVs, year)


def _get_trajectories_one_thread(
    society_class: Type[Society],
    society_kwargs,
    T: int,
    MC: int,
) -> List[DataFrame]:
    trajectories = []
    for _ in range(MC):
        society = society_class(**society_kwargs)
        society.run(T - 1)
        trajectories.append(society.get_historical_states())
    return trajectories


def _get_trajectories_multi_threads(
    society_class: Type[Society],
    society_kwargs,
    T: int,
    MC: int,
    threads: int,
) -> List[DataFrame]:
    pool = Pool(threads)
    pickled_function = lambda args: _get_trajectories_one_thread(*args)  # noqa
    args_list = [[society_class, society_kwargs, T, MC // threads]] * threads
    args_list[-1][-1] = MC - (threads - 1) * (MC // threads)
    _ret = pool.map(pickled_function, args_list)
    ret = []
    for lt in _ret:
        ret.extend(lt)
    return ret


def check_by(
    society_class: Type[Society],
    society_kwargs,
    param: str,
    param_list: list,
    T: int,
    MC: int,
    threads: int,
) -> Dict[str, Tuple[List[DataFrame], List[DataFrame], List[DataFrame], DataFrame]]:
    """The function counts trajectories for different parameters.
    The function counts MC trajectories for each value of parameter
        (param) in the list param_list. See get_trajectories.

    Args:
        society_class (Type[Society]): Society class for run simulations.
        society_kwargs (_type_): Deflaut kwargs for Society.
        param (str): The name of the parameter that changes with different simulations.
        param_list (list): Parameter values that are assumed in different simulations.
        T (int): Time horizont for single simulation.
        MC (int): MC repetitions.
        threads (int): Threads to use in multithreads run.

    Raises:
        AttributeError: Param must be key from CommonParamsKwargs or "society"

    Returns:
        Dict[str, Tuple[List[DataFrame], List[DataFrame], List[DataFrame], DataFrame]]: _description_
    """
    ret = {}
    if param in society_kwargs:
        for el in tqdm(param_list):
            tmp_society_kwargs = society_kwargs.copy()
            tmp_society_kwargs[param] = el
            if param == "government":
                name = f"{el}".split(".")[-1].split(" ")[0]
            else:
                name = f"{el}"
            ret[name] = get_trajectories(
                society_class,
                tmp_society_kwargs,
                T,
                MC,
                threads,
            )
    elif param.lower() == "society":
        for soc in tqdm(param_list):
            ret[f"{soc.__name__}"] = get_trajectories(
                soc,
                society_kwargs,
                T,
                MC,
                threads,
            )
    else:
        raise AttributeError(
            f'Param must be key from CommonParamsKwargs or "society", not {param}'
        )
    return ret
