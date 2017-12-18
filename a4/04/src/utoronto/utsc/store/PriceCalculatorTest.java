import org.junit.Before;
import org.junit.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;

public class PriceCalculatorTest {

    private Priced usbStick;
    private List<Priced> stuff;

    @Before
    public void setUp() throws Exception {
        usbStick = new Product("234523452345", 35);
        stuff = Arrays.asList(new Priced [] {usbStick});
    }

    @Test
    public void getTotalPrice() throws Exception {
        PriceCalculator pc = new PriceCalculator(new MockDiscount());
        assertEquals("Priced should be 30", 30, pc.getTotalPrice(stuff), 0);
    }

}
