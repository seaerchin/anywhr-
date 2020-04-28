
import types
from typing import List, Tuple, DefaultDict, Dict
from constants import border_translation
from collections import defaultdict

# global to hold all hexagons created 
hexagons:Dict[str, "hexagon"] = {}

class hexagon():
    """
    models a hexagon; the hexagon has CRUD operations.
    """ 

    # hexagon needs to have 6 borders 
    # kwargs represents neighbours as tuples eg (2, dx)
    def __init__(self, name: str, **kwargs: Dict[str, Tuple[int, str]]):
        """ creates a hexagon with the specified name; extra arguments specify its neighbours """ 
        self.name = name
        self.neighbours:Dict[int, "hexagon"] = {}
        if kwargs: 
            for i in kwargs["neighbours"]:
                self.__insert_neighbour(i[0], hexagons[i[1]])
    
    def __str__(self):
        """ returns the string representation of the hexagon """ 
        return self.name
    
    def query(self) -> List[Tuple[int, str]]:
        """ returns the neighbours of this hexagon, sorted by border number """ 
        i = self.neighbours.items()
        return sorted(map(lambda x: (x[0], str(x[1])), i), key = lambda x: x[0])

    def __add_neighbour(self, border: int, target: "hexagon"):
        """ adds a new neighbour at the specified border; this is mirrored on the other hexagon """ 
        # translate 
        self.neighbours[border] = target
        target.neighbours[border_translation[border]] = self

    # borders contains your next path to traverse 
    # to_add is the hexagon to add 
    def __update_neighbours(self, borders: List[int], to_add: "hexagon"):
        """ updates your neighbours to add the target hexagon (to_add) using the given border path """ 
        # index to add at is given by next + 1 % 6 
        if borders: 
            next = borders.pop(0)
            idx = (next + 1) % 6
            self.__add_neighbour(idx, to_add)
            try: 
                self.neighbours[next].__update_neighbours(borders, to_add)
            except KeyError: 
                print("neighbour {} of {} does not exist".format(next, self.name))
            
    def __insert_neighbour(self, border: int, hexa: "hexagon") -> None:
        """ informs the node that there is a new node added and recursively updates the concerned nodes """ 
        center_border = border_translation[border]
        paths = [i for i in range(6)]
        # path that i need to traverse starting from this hexagon
        update_path = rotate(paths, center_border)
        self.__update_neighbours(update_path, hexa)

    def __inform_neighbours(self, border:int, hexa: "hexagon"):
        """ informs the neighbours of the inserted hexagon to add the new hexagon to their neighbours """ 
        bordering = [((border - 1) % 6, 1), ((border + 1) % 6, -1)]
        for i in bordering: 
            try: 
                neighbour = self.neighbours[i[0]]
                neighbour.__insert_neighbour((border + i[1]) % 6, hexa)
            except KeyError:
                # neighbour at border i doesn't exist
                continue 

    def add_neighbour(self, border: int, hexa: "hexagon"):
        """ adds the hexagon at the given border """ 
        self.__insert_neighbour(border, hexa)
        self.__inform_neighbours(border, hexa)

def rotate(list: List[int], border:int) -> List[int]:
    """ rotates a list to the border number so that it gives the border path to traverse """ 
    num_rotate = (border + 2) % 6
    return list[num_rotate:]+list[:num_rotate]

# whether you can remove the hexagon in question
def valid_remove(target: hexagon) -> bool:
    """ checks whether the specified hexagon can be removed """ 
    num_remove = len(hexagons)
    if num_remove < 2:
        return True
    # recur on any single neighbour 
    neighbours = list(target.neighbours.values())
    if len(neighbours) < 2:
        return True 
    neighbour = neighbours[0]
    dp:DefaultDict[str, bool] = defaultdict(bool)
    # from random neighbour -> mark neighbour has seen
    # traverse to all neighbours 
    # return size 
    def dfs(neighbour: hexagon, count:int = 0) -> int:
        # this is o(n) time/space but we utilize a dict to store seen nodes
        for i in neighbour.neighbours.values(): 
            # different from original and unseen 
            if i.name != target.name and not dp[i.name]:
                count += 1
                dp[i.name] = True 
                count += dfs(i)
        return count 
    cnt = dfs(neighbour)
    return cnt + 1 == num_remove 

def remove(target: str) -> bool:
    """ removes the specified hexagon from the global state as well as its neighbours; note that no further reference will be held to this hexagon """ 
    target_hexagon = hexagons[target]
    if valid_remove(target_hexagon):
        del hexagons[target_hexagon.name]
        for border, hexa in target_hexagon.neighbours.items(): 
            del hexa.neighbours[border_translation[border]]
        return True
    return False
