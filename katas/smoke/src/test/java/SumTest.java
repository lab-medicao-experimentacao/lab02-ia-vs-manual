import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
class SumTest {
    @Test void positive() { assertEquals(5, Sum.add(2, 3)); }
    @Test void negative() { assertEquals(-5, Sum.add(-2, -3)); }
    @Test void zero() { assertEquals(0, Sum.add(0, 0)); }
}
