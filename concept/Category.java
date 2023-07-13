import java.util.List;

public class Category extends node {

    public List<node> children;

    public Category(Integer id, String name, node mother) {
        super(id, name, mother);
    }

    public Category(Integer id, String name, node mother, List<node> children) {
        super(id, name, mother);
        this.children = children;
    }

    public Category() {
    }

    public List<node> getChildren() {
        return children;
    }

    public void setChildren(List<node> children) {
        this.children = children;
    }

    public Boolean hasMother() {
        return this.mother != null;
    }

    @Override
    public String toString() {
        return "Category{" +
                "children=" + children +
                ", id=" + id +
                ", name='" + name + '\'' +
                ", mother=" + mother +
                '}';
    }
}
