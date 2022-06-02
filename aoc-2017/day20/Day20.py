from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        particles = []
        for line in map(lambda x: x.rstrip(), input_file.readlines()):
            particles.append(tuple(map(lambda t: tuple(map(int, t[3:-1].split(','))), line.split(', '))))
        return particles


@timed
def part1(particles):
    print(particles.index(min(particles, key=lambda p: abs(p[2][0]) + abs(p[2][1]) + abs(p[2][2]))))


@timed
def part2(particles):
    prev_count = 0
    countdown = 0
    while True:
        seen = set()
        new_particles = []
        for (x_pos, y_pos, z_pos), (x_vel, y_vel, z_vel), (x_acc, y_acc, z_acc) in particles:
            x_vel += x_acc
            y_vel += y_acc
            z_vel += z_acc

            x_pos += x_vel
            y_pos += y_vel
            z_pos += z_vel

            if (x_pos, y_pos, z_pos) not in seen:
                seen.add((x_pos, y_pos, z_pos))
                new_particles.append(((x_pos, y_pos, z_pos), (x_vel, y_vel, z_vel), (x_acc, y_acc, z_acc)))
            else:
                if a := [p for p in new_particles if p[0] == (x_pos, y_pos, z_pos)]:
                    new_particles.remove(a.pop())

        particles = new_particles

        if (new_count := len(particles)) != prev_count:
            prev_count = new_count
            countdown = 0
        elif countdown == 8:
            print(prev_count)
            return
        else:
            countdown += 1


if __name__ == '__main__':
    particle_list = read()
    part1(particle_list)
    part2(particle_list)
