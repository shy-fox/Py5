class Arrays:
    @staticmethod
    def fill(arr: list[any], val: any) -> list[any]:
        for i in range(len(arr)):
            arr[i] = val
        return arr
