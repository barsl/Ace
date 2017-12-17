package ca.utoronto.utsc.store.products;

public class Product implements Priced {

    private double price;
    private String isbn;

    public double getPrice() {
        return this.price;
    }

    public Product(String isbn, double price) {
        this.isbn = isbn;
        this.price = price;
    }


}
