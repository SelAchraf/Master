package cache_proxy;

public class RealUrlRetreiver implements InterfaceUrlRetreiver{

	@Override
	public String getPage(String url) {
		System.out.println("From real retreiver");
		return "<html>" + url + "</html>";
	}

}