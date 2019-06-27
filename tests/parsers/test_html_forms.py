import responses
import requests

from wapitiCore.net.crawler import Page


@responses.activate
def test_forms():
    with open("tests/data/forms.html") as fd:
        url = "http://perdu.com/"
        responses.add(
            responses.GET,
            url,
            body=fd.read()
        )

        resp = requests.get(url, allow_redirects=False)
        page = Page(resp, url)
        count = 0
        form_action = False

        for form in page.iter_forms():
            count += 1
            if form.file_path == "/get_form":
                assert form.method == "GET"
                assert form.url == "http://perdu.com/get_form?name=default"
                assert form.referer == "http://perdu.com/"
                assert len(form.get_params) == 1
                assert not len(form.post_params)
                assert not len(form.file_params)
                assert not form.is_multipart
            elif form.file_path == "/post_select.php":
                assert form.method == "POST"
                assert form.get_params == [["id", "3"]]
                assert form.post_params == [["fname", "Smith"], ["csrf", "9877665"], ["carlist", "volvo"]]
                assert form.url == "http://perdu.com/post_select.php?id=3"
                assert not form.is_multipart
                assert not len(form.file_params)
            elif form.file_path == "/fields.php":
                assert form.method == "POST"
                assert not form.is_multipart
                assert dict(form.post_params) == {
                    "vehicle1": "car",
                    "vehicle2": "boat",
                    "color": "#bada55",
                    "date": "2019-03-03",
                    "datetime": "2019-03-03T20:35:34.32",
                    "datetime-local": "2019-03-03T22:41",
                    "email": "wapiti2019%40mailinator.com",
                    "file": "pix.gif",
                    "gender": "other",  # taking the last one
                    "hidden": "default",
                    "image.x": "1",
                    "image.y": "1",
                    "month": "2019-03",
                    "number": "1337",
                    "password": "letmein",
                    "radio": "beton",
                    "range": "37",
                    "search": "default",
                    "submit": "submit",
                    "tel": "0606060606",
                    "text": "default",
                    "textarea": "Hi there!",
                    "time": "13:37",
                    "url": "http://wapiti.sf.net/",
                    "week": "2019-W24"
                }
            elif form.file_path == "/upload.php":
                assert form.is_multipart
                assert not form.post_params
                assert form.file_params == [["file", ["pix.gif", "GIF89a", "image/gif"]]]
            elif form.file_path == "/alt.php":
                form_action = True
            else:
                # Form with no action set
                assert form.file_path == "/"

        assert count == 6
        assert form_action