import java.util.ArrayList;
import java.util.List;

public class test {
    public static void main(String[] args) {
        Category employee = new Category(1, "Employee", null);
        Category professor = new Category(2, "Professor", employee);
        Category tutor = new Category(3, "Tutor", employee);
        Category student = new Category(4, "Student", null);

        List<User> professors = new ArrayList<>();
        User user1 = new User(100, "Thomas", professor);
        professors.add(user1);

        List<User> tutors = new ArrayList<>();
        User user2 = new User(101, "Alex", tutor);
        tutors.add(user2);

        List<User> students = new ArrayList<>();
        User user3 = new User(102, "Mike", student);
        students.add(user3);

        System.out.println(user1);
        System.out.println(user2);
        System.out.println(user3);

    }
}
