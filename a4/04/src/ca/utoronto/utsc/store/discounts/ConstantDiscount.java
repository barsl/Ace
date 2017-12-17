package ca.utoronto.utsc.store.discounts;

public class ConstantDiscount implements Discount {

    private double amount;

    public ConstantDiscount(double amount) {
        this.amount = amount;
    }

    public double getDiscountedPrice(double price) {
        return (price - this.amount);
    }
}
