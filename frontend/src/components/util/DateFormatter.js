class DateFormatter {
  constructor() {}

  formatMonth(month) {
    return this.formatNumber(++month);
  }

  formatNumber(num) {
    if (num < 10) num = "0" + num;
    return num;
  }

  getPrettyDate(date) {
    if (date instanceof Date) {
      const year = date.getFullYear();
      const month = this.formatMonth(date.getMonth());
      const day = this.formatNumber(date.getDate());

      const hour = this.formatNumber(date.getHours());
      const minutes = this.formatNumber(date.getMinutes());
      return year + "-" + month + "-" + day + " " + hour + ":" + minutes;
    } else throw "Parameter is not date!";
  }
}

export default new DateFormatter();
