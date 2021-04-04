import pygame

class Snake:
    is_alive = True
    grow_at_next_move = False

    def __init__(self, segments, color, direction, board):
        self.segments = segments
        self.color = color
        self.direction = direction
        self.board = board
        head_path = '../assets/snek-head-' + color + '.png'
        body_path = '../assets/snek-body-' + color + '.png'
        bent_body_path = '../assets/snek-bent-body-' + color + '.png'
        tail_path = '../assets/snek-tail-' + color + '.png'
        self.head_texture = pygame.image.load(head_path)
        self.body_texture = pygame.image.load(body_path)
        self.bent_body_texture = pygame.image.load(bent_body_path)
        self.tail_texture = pygame.image.load(tail_path)

        for segment in self.segments:
            field_to_place = self.board.request_field(segment)
            field_to_place.place_snake(self)

    def draw_segment(self, frame, draw_coords, side_length, segment_coords):
        # Wyjątek segment_coords poza segments

        if not self.is_alive:
            return

        if self.segments[-1] == segment_coords:
            resized_head_texture = pygame.transform.scale(self.head_texture, (field_side, field_side))
            if str(self.direction) == 'N':
                segment_texutre = resized_head_texture
            elif str(self.direction) == 'E':
                segment_texutre = pygame.transform.rotate(resized_head_texture, -90)
            elif str(self.direction) == 'S':
                segment_texutre = pygame.transform.rotate(resized_head_texture, -180)
            else:
                segment_texutre = pygame.transform.rotate(resized_head_texture, -270)   
        elif self.segments[0] == segment_coords:
            possible_direcitons = ['N', 'E', 'S', 'W']
            tail_coords = self.segments[0]
            last_body_coords = self.segments[1]

            for direction_letter in possible_direcitons:
                direction = Direction(direction_letter)
                if direction.move_in_direction(tail_coords) == last_body_coords:
                    break

            result_direction = str(direction)

            resized_tail_texture = pygame.transform.scale(self.tail_texture, (field_side, field_side))

            if result_direction == 'N':
                segment_texutre = resized_tail_texture
            elif result_direction == 'E':
                segment_texutre = pygame.transform.rotate(resized_tail_texture, -90)
            elif result_direction == 'S':
                segment_texutre = pygame.transform.rotate(resized_tail_texture, -180)
            else:
                segment_texutre = pygame.transform.rotate(resized_tail_texture, -270)
        else:
            possible_direcitons = ['N', 'E', 'S', 'W']
            current_segment_coords = segment_coords
            prev_segment_coords = self.segments[self.segments.index(segment_coords) + 1]
            next_segment_coords = self.segments[self.segments.index(segment_coords) - 1]

            for direction_letter in possible_direcitons:
                direction = Direction(direction_letter)
                if direction.move_in_direction(current_segment_coords) == prev_segment_coords:
                    prev_direction = str(direction)

                if direction.move_in_direction(current_segment_coords) == next_segment_coords:
                    next_direction = str(direction)

            direction_string = prev_direction + next_direction

            if direction_string == 'NS' or direction_string == 'SN':
                resized_body_texture = pygame.transform.scale(self.body_texture, (field_side, field_side))
                segment_texutre = resized_body_texture
            elif direction_string == 'WE' or direction_string == 'EW':
                resized_body_texture = pygame.transform.scale(self.body_texture, (field_side, field_side))
                segment_texutre = pygame.transform.rotate(resized_body_texture, -90)
            elif direction_string == 'NE' or direction_string == 'EN':
                resized_body_texture = pygame.transform.scale(self.bent_body_texture, (field_side, field_side))
                segment_texutre = pygame.transform.rotate(resized_body_texture, -180)
            elif direction_string == 'ES' or direction_string == 'SE':
                resized_body_texture = pygame.transform.scale(self.bent_body_texture, (field_side, field_side))
                segment_texutre = pygame.transform.rotate(resized_body_texture, 90)
            elif direction_string == 'SW' or direction_string == 'WS':
                resized_body_texture = pygame.transform.scale(self.bent_body_texture, (field_side, field_side))
                segment_texutre = resized_body_texture
            elif direction_string == 'WN' or direction_string == 'NW':
                resized_body_texture = pygame.transform.scale(self.bent_body_texture, (field_side, field_side))
                segment_texutre = pygame.transform.rotate(resized_body_texture, -90)
            else:
                raise Exception("Bad segment orientation")

        frame.blit(segment_texutre, draw_coords)

    def move(self):
        current_head_coords = self.segments[-1]
        new_head_coords = self.direction.move_in_direction(current_head_coords)
        new_field = self.board.request_field(new_head_coords)

        if not new_field.check_snake_move(self):
            self.destroy()
            return

        if not self.grow_at_next_move:
            field_to_remove = self.board.request_field(self.segments[0])
            field_to_remove.remove_snake(self)
            self.segments.pop(0)
        else:
            self.grow_at_next_move = False

        self.segments.append(new_head_coords)
        new_field.snake_entered(self, self.direction)

    def grow(self):
        self.grow_at_next_move = True

    def destroy(self):
        for segment_coords in self.segments:
            field = self.board.request_field(segment_coords)
            field.remove_snake(self)
        self.is_alive = False

    def interact_with_snake(self, other_snake):
        snake_head_coords = self.segments[-1]
        other_head_coords = other_snake.segments[-1]
        if snake_head_coords == other_head_coords:
            self.destroy()
        other_snake.destroy()
