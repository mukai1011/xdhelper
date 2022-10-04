from datetime import timedelta
from typing import List, Tuple

from .current_seed_searcher import CurrentSeedSearcher
from .protocol import Operation
from .util import get_wait_time, is_suitable_for_waiting

class TargetDecider():
    """初期seed厳選を行い、目標seedを決定する。
    """
    def __init__(self, current_seed_searcher: CurrentSeedSearcher, transition_to_quick_battle: Operation[None]) -> None:
        """
        Args:
            current_seed_searcher (CurrentSeedSearcher): 
            transition_to_quick_battle (Operation[None]): リセットし、1回いますぐバトル（さいきょう）を生成した画面まで誘導する
            tsv (Optional[int]): _description_
        """
        self.__current_seed_searcher = current_seed_searcher
        self.__transition_to_quick_battle = transition_to_quick_battle

    def execute(self, target_seeds: List[int]) -> Tuple[int, Tuple[int, timedelta]]:
        """
        Args:
            target_seeds (List[int]): 目標seedのリスト

        Returns:
            Tuple[int, Tuple[int, timedelta]]: 現在のseedと「目標のseedと待機時間のタプル」のタプル
        """
        current_seed: int = int()
        target: Tuple[int, timedelta] = (int(), timedelta())

        while True:
            self.__transition_to_quick_battle.run()
            try:
                current_seed = self.__current_seed_searcher.search()
            except:
                continue
            
            target = sorted(
                [(target_seed, get_wait_time(current_seed, target_seed)) for target_seed in target_seeds]
            )[0]
            
            if is_suitable_for_waiting(target[1]):
                break
        return current_seed, target