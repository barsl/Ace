public class MockDiscount implements Discount {

    @Override
    public double getDiscountedPrice(double price) {
        return price - 5;
    }
}
