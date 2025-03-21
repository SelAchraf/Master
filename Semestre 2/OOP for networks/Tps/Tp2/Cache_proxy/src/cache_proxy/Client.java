package cache_proxy;

import java.util.concurrent.TimeUnit;

public class Client {

	public static void main(String[] args) throws InterruptedException {
		InterfaceUrlRetreiver u = new ProxyUrlRetreiver();
		String page = u.getPage("google.com");
		System.out.println(page);

		TimeUnit.SECONDS.sleep(2);
		
		page = u.getPage("google.com");
		System.out.println(page);
	}

}