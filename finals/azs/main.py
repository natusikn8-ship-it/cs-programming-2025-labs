from ui.menu import MainMenu

def main():
    """Точка входа в программу"""
    try:
        # Создание и запуск главного меню
        menu = MainMenu()
        menu.run()
        
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем (Ctrl+C)")
        print("Данные сохранены. До свидания!")
        
if __name__ == "__main__":
    main()
