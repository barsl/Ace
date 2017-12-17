
import java.util.Date;


public class SeasonalDiscount extends CalendarDiscount{

    private java.util.Date from;
    private java.util.Date to;

    public SeasonalDiscount(double rate, java.util.Date from, java.util.Date to) {
        super(rate);
        this.from = from;
        this.to = to;
    }

    public boolean isApplicableToday() {
        Date today = new Date();
        boolean result = false;
        if ((today.compareTo(this.from) >= 0) && (today.compareTo(this.to) < 0)) {
            // if the date is in between the from and to dates
            result = true;
        }
        return result;
    }
}
