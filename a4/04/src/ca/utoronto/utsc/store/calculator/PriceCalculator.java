package ca.utoronto.utsc.store.calculator;

import java.util.List;

public class PriceCalculator {

    private Discount discount;
    public PriceCalculator(Discount discount) {
        this.discount = discount;
    }

    public double getTotalPrice(List<Priced> items){
        double result = 0;
        for (int i=0; i < items.size(); i++) {
            result += discount.getDiscountedPrice(items.get(i).getPrice());
        }
        return result;
    }
}
