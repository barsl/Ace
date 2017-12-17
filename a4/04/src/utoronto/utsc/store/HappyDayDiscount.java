import java.util.Calendar;
import java.util.Date;

public class HappyDayDiscount extends CalendarDiscount {

    private int happyDay;

    public HappyDayDiscount(double rate, int day) {
        super(rate);
        this.happyDay = day;
    }

    public boolean isApplicableToday() {
        boolean result = false;
        // get todays day of the week
        Date today = new Date();
        Calendar date = Calendar.getInstance();
        date.setTime(today);
        // get the day of the week as a number
        int todayNum = date.get(Calendar.DAY_OF_WEEK);
        if (todayNum == this.happyDay) {
            result = true;
        }
        return result;
    }
}
