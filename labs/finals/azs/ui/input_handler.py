from typing import Optional, Tuple

class InputHandler:
    def get_int_input(self, prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None, allow_cancel: bool = False) -> Optional[int]:
        while True:
            value = input(prompt).strip()
            
            if allow_cancel and value == "":
                return None
            
            try:
                num = int(value)
            except ValueError:
                print("Введите целое число")
                continue
            
            if min_val is not None and num < min_val:
                print(f"Число должно быть не меньше {min_val}")
                continue
            
            if max_val is not None and num > max_val:
                print(f"Число должно быть не больше {max_val}")
                continue
            
            return num
    
    def get_float_input(self, prompt: str, min_val: Optional[float] = None, max_val: Optional[float] = None, allow_cancel: bool = False) -> Optional[float]:
        while True:
            value = input(prompt).strip()
            
            if allow_cancel and value == "":
                return None
            
            try:
                num = float(value)
            except ValueError:
                print("Введите число")
                continue
            
            if min_val is not None and num < min_val:
                print(f"Число должно быть не меньше {min_val}")
                continue
            
            if max_val is not None and num > max_val:
                print(f"Число должно быть не больше {max_val}")
                continue
            
            return num
    
    def get_positive_float(self, prompt: str, allow_cancel: bool = False) -> Optional[float]:
        return self.get_float_input(prompt, min_val=0.001, allow_cancel=allow_cancel)
    
    def get_menu_choice(self, prompt: str, min_choice: int, max_choice: int) -> int:
        return self.get_int_input(prompt, min_choice, max_choice)
    
    def get_yes_no(self, prompt: str, default: Optional[bool] = None) -> bool:
        if default is True:
            prompt += " (Y/n): "
        elif default is False:
            prompt += " (y/N): "
        else:
            prompt += " (y/n): "
        
        while True:
            value = input(prompt).strip().lower()
            
            if value == "" and default is not None:
                return default
            
            if value in ['y', 'yes', 'д', 'да']:
                return True
            
            if value in ['n', 'no', 'н', 'нет']:
                return False
            
            print("Введите 'y' (да) или 'n' (нет)")
    
    def get_string_input(self, prompt: str, allow_empty: bool = False) -> str:
        while True:
            value = input(prompt).strip()
            
            if value or allow_empty:
                return value
            else:
                print("Строка не может быть пустой")
    
    def select_from_list(self, prompt: str, items: list, display_func=None) -> Tuple[int, any]:
        print()
        for i, item in enumerate(items, 1):
            if display_func:
                display_text = display_func(item)
            else:
                display_text = str(item)
            
            print(f"{i}) {display_text}")
        
        print()
        choice = self.get_menu_choice(prompt, 1, len(items))
        
        return choice - 1, items[choice - 1]
    
    def confirm_operation(self, message: str) -> bool:
        print(f"\n{message}")
        return self.get_yes_no("Подтвердить операцию?")
