public abstract class CalendarDiscount implements Discount {

    private double discountRate;

    public CalendarDiscount(double rate) {
        this.discountRate = rate;
    }

    public double getDiscountedPrice(double price) {
        if (isApplicableToday()) {
            return (1 - this.discountRate) * price;
        } else {
            return price;
        }
    }

    public abstract boolean isApplicableToday();
}
