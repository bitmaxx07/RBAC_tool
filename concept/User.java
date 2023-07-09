public class User extends node {
    public User(Integer id, String name, node mother) {
        super(id, name, mother);
    }

    public User() {
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", mother=" + mother +
                '}';
    }
}
