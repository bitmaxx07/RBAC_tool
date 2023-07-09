public class node {

    public Integer id;
    public String name;
    public node mother;

    public node(Integer id, String name, node mother) {
        this.id = id;
        this.name = name;
        this.mother = mother;
    }

    public node() {
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public node getMother() {
        return mother;
    }

    public void setMother(node mother) {
        this.mother = mother;
    }

    @Override
    public String toString() {
        return "node{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", mother=" + mother +
                '}';
    }
}
