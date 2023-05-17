import dataclasses

from main.models import AppUser, ScheduleTableCell

TIMES = [
    '10:00 - 11: 00',
    '11: 00 - 12:00',
    '12: 00 - 13:00',
    '13: 00 - 14:00',
    '15: 00 - 16:00',
    '16: 00 - 17:00',
    '17: 00 - 18:00',
    '18: 00 - 19:00',
    '19: 00 - 20:00',
    '20: 00 - 21:00',
    '22: 00 - 23:00',
    '23: 00 - 00:00',
]

WEEK_DAYS = [
    ScheduleTableCell.MONDAY,
    ScheduleTableCell.TUESDAY,
    ScheduleTableCell.WEDNESDAY,
    ScheduleTableCell.THURSDAY,
    ScheduleTableCell.FRIDAY,
    ScheduleTableCell.SATURDAY,
    ScheduleTableCell.SUNDAY,
]


@dataclasses.dataclass
class Cell:
    row: str
    col: str

    html_class: str


def get_html_class(
    user: AppUser,
    week_day: int,
    row_number: int,
) -> str:
    cell = ScheduleTableCell.objects.filter(
        teacher=user,
        week_day=week_day,
        row_number=row_number,
    ).first()

    if cell:
        return cell.html_class

    return ''


def generate_table(user: AppUser) -> list[tuple[str, list[Cell]]]:
    time_and_cells_list = []

    for row_number, time in enumerate(TIMES, start=1):
        cells = []

        for week_day in WEEK_DAYS:
            html_class = get_html_class(user, week_day, row_number)

            cells.append(Cell(
                row=row_number,
                col=week_day,
                html_class=html_class
            ))

        time_and_cells_list.append((time, cells))

    return time_and_cells_list
