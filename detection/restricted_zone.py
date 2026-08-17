from config.settings import (
    ZONE_X1,
    ZONE_Y1,
    ZONE_X2,
    ZONE_Y2
)


def check_restricted_zone(person_boxes):
    """
    Check whether any detected person has entered
    the restricted zone.

    Returns:
        restricted_breach: True if a person is inside the zone
    """

    restricted_breach = False

    for x1, y1, x2, y2 in person_boxes:

        # Center of person's bounding box
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        inside_zone = (
            ZONE_X1 < center_x < ZONE_X2
            and
            ZONE_Y1 < center_y < ZONE_Y2
        )

        if inside_zone:

            restricted_breach = True

    return restricted_breach