package cache_proxy;

import java.util.HashMap;
import java.util.Map;

public class ProxyUrlRetreiver implements InterfaceUrlRetreiver{
	InterfaceUrlRetreiver real = new RealUrlRetreiver();
	Map<String, String> UrlToPage = new HashMap<String, String>();
	Map<String, Integer> UrlToTime = new HashMap<String, Integer>();

	@Override
	public String getPage(String url) {
		if (UrlToTime.containsKey(url)) {
			int lastRetreived = UrlToTime.get(url);
			if (((int) System.currentTimeMillis() - lastRetreived) < 8000) {
				System.out.println("From proxy cache");

				return UrlToPage.get(url);
			}
			else {
				String page = this.real.getPage(url);
				UrlToTime.put(url, (int) System.currentTimeMillis());
				UrlToPage.put(url, page);
				return page;
			}
		}
		else {
			String page = this.real.getPage(url);
			UrlToTime.put(url, (int) System.currentTimeMillis());
			UrlToPage.put(url, page);
			return page;
		}
	}

}