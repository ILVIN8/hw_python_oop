from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: int

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    training_type = 'Не определен'

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.training_type,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    training_type = 'Running'
    coeff_calories_for_run_1 = 18
    coeff_calories_for_run_2 = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        time_in_min = self.duration * 60
        spent_calories = ((self.coeff_calories_for_run_1
                          * self.get_mean_speed()
                          - self.coeff_calories_for_run_2)
                          * self.weight / self.M_IN_KM
                          * time_in_min)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_type = 'SportsWalking'
    coeff_calories_for_walk_1 = 0.035
    coeff_calories_for_walk_2 = 0.029
    degree = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        time_in_min = self.duration * 60
        spent_calories = (
            (self.coeff_calories_for_walk_1 * self.weight
             + (self.get_mean_speed() ** self.degree // self.height)
             * self.coeff_calories_for_walk_2 * self.weight) * time_in_min
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    training_type = 'Swimming'
    LEN_STEP = 1.38
    coeff_calories_for_swim_1 = 1.1
    coeff_calories_for_swim_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool
                      * self.count_pool / self.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed()
                          + self.coeff_calories_for_swim_1)
                          * self.coeff_calories_for_swim_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    workout_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in workout_dict:
        raise ValueError(f'Error. Ключи {workout_dict.keys()} не найдены')
    else:
        data_class = workout_dict[workout_type]
        return data_class(*data)


def main(training: Training) -> None:
    """Главная функция."""
    show = training.show_training_info()
    info = show.get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
