import io
import os
import re
import base64
from urllib.parse import quote, unquote
import zipfile
import tempfile
import shutil
from apps.medias.models import Media
from apps.medias.serializers import MediaSerializer
from django.core.files.base import ContentFile
from django.core.files import File
from apps.organizations.models import Organization
import mammoth

from .omml import omml2tex, omml2mml
from bs4 import BeautifulSoup
import bs4

_omath_pattern = re.compile(r"<m:oMath[^<>]*>.+?</m:oMath>", flags=re.S)
_omath_para_pattern = re.compile(r"<m:oMathPara\s*>(.+?)</m:oMathPara>", flags=re.S)

_equation_pattern = re.compile(r'<span class="equation">.+?</span>', flags=re.S)
_image_html_pattern = re.compile(r"<img src=.+? />", flags=re.S)

import logging
from django.utils.timezone import now

logger = logging.getLogger(__name__)


class EquationMarkDown:
    start = "!!![equation]("
    end = ")!!!"


class SubscriptMarkDown:
    start = "!!![sub]("
    end = ")!!!"


class SuperscriptMarkDown:
    start = "!!![sup]("
    end = ")!!!"


def quote_omath(xml_content):
    def replace(match):
        quoted_omath = quote(match.group(0))
        return "<w:t>$omml$ {} $/omml$</w:t>".format(quoted_omath)

    xml_content = _omath_pattern.sub(replace, xml_content)
    xml_content = _omath_para_pattern.sub(lambda m: m.group(1), xml_content)
    return xml_content


def quote_mml(xml_content):
    def replace(match):
        quoted_mml = quote(match.group(0))
        return "$mml$ {} $/mml$".format(quoted_mml)

    xml_content = _equation_pattern.sub(replace, xml_content)
    return xml_content


def unquote_mml(html):
    def replace(match):
        list_match = _mml_pattern.findall(match.group(0))
        if list_match:
            match = list_match[0]
        mml_content = unquote(match)
        return mml_content

    result = _mml_pattern.sub(replace, html)

    return result


def quote_img(xml_content):
    def replace(match):
        quoted_mml = quote(match.group(0))
        return "$img$ {} $/img$".format(quoted_mml)

    xml_content = _image_html_pattern.sub(replace, xml_content)
    return xml_content


def unquote_img(html):
    def replace(match):
        list_match = _img_pattern.findall(match.group(0))
        if list_match:
            match = list_match[0]
        img_content = unquote(match)
        return img_content

    result = _img_pattern.sub(replace, html)

    return result


_omml_pattern = re.compile(r"\$omml\$(.+?)\$/omml\$")
_mml_pattern = re.compile(r"\$mml\$(.+?)\$/mml\$")
_img_pattern = re.compile(r"\$img\$(.+?)\$/img\$")


def convert_quoted_omath_to_tex(html):
    def replace(match):
        omml_content = unquote(match.group(1))
        return omml2tex(omml_content)

    return _omml_pattern.sub(replace, html)


def convert_quoted_omath_to_mml(html):
    def replace(match):
        omml_content = unquote(match.group(1))
        mml_content = omml2mml(omml_content)

        return '<span class="equation">{}</span>'.format(mml_content)

    return _omml_pattern.sub(replace, html)


def pre_process_docx(docx_filename):
    name_ext = list(os.path.splitext(docx_filename))
    name_ext.insert(1, "_copy")
    new_docx_filename = "".join(name_ext)

    document_filename = "word/document.xml"
    with zipfile.ZipFile(docx_filename) as z_in:
        with zipfile.ZipFile(new_docx_filename, "w") as z_out:
            z_out.comment = z_in.comment
            for item in z_in.infolist():
                if item.filename != document_filename:
                    z_out.writestr(item, z_in.read(item.filename))
            document_xml = z_in.read(document_filename).decode("utf8")
            document_xml = quote_omath(document_xml).encode("utf8")
            z_out.writestr(document_filename, document_xml)
    # mismatch tags error occurs
    return new_docx_filename


def pre_process_docx_from_file(file, temporary_directory):
    # Create new file name
    name_ext = list(os.path.splitext(file.name))
    name_ext.insert(1, "_copy")
    new_docx_filename = "".join(name_ext)
    new_docx_file_path = os.path.join(temporary_directory, new_docx_filename)

    document_filename = "word/document.xml"
    with zipfile.ZipFile(file) as z_in:
        with zipfile.ZipFile(new_docx_file_path, "w") as z_out:
            z_out.comment = z_in.comment
            for item in z_in.infolist():
                if item.filename != document_filename:
                    z_out.writestr(item, z_in.read(item.filename))
            document_xml = z_in.read(document_filename).decode("utf8")
            document_xml = quote_omath(document_xml).encode("utf8")
            z_out.writestr(document_filename, document_xml)
    return new_docx_file_path


def convert_to_html(docx_filename):
    new_docx_filename = pre_process_docx(docx_filename)
    with open(new_docx_filename, "rb") as file:
        res = mammoth.convert_to_html(file)
    os.remove(new_docx_filename)
    html = convert_quoted_omath_to_mml(res.value)
    return html


class ImageWriter(object):
    def __init__(self, output_dir):
        self._output_dir = output_dir
        self._image_number = 1

    def __call__(self, element):
        extension = element.content_type.partition("/")[2]
        image_filename = "{0}.{1}".format(self._image_number, extension)
        with open(os.path.join(self._output_dir, image_filename), "wb") as image_dest:
            with element.open() as image_source:
                shutil.copyfileobj(image_source, image_dest)

        self._image_number += 1

        return {"src": image_filename}


def convert_to_html_from_file(file):
    html = None
    # Create a temporary directory
    temporary_directory = tempfile.mkdtemp()

    def convert_image(image):
        # fix upload url
        org_ecoms = Organization.objects.only("id").filter(name="Ecoms").first()
        image.alt_text = None
        # Create new file name
        temporary_image_name = temporary_directory
        with image.open() as image_bytes:
            temporary_image_name = os.path.join(
                temporary_directory, os.path.basename(image_bytes.name)
            )
            with open(temporary_image_name, mode="wb") as temp_image:
                temp_image.write(image_bytes.read())
            local_file = open(temporary_image_name, "rb")
            djangofile = File(local_file)
            image_bytes_name, file_extension = os.path.splitext(image_bytes.name)
            djangofile.name = now().strftime("%Y%m%d__%H%M%S") + file_extension
            media_instance = Media(resource=djangofile, organization=org_ecoms)
            media_instance.save()
        return {"src": "{}".format(media_instance.resource.url)}

    try:
        new_docx_file_path = pre_process_docx_from_file(file, temporary_directory)
        with open(new_docx_file_path, "rb") as file:
            img_element = mammoth.images.img_element(convert_image)
            res = mammoth.convert_to_html(file, convert_image=img_element)
            html = convert_quoted_omath_to_mml(res.value)
    finally:
        shutil.rmtree(temporary_directory)
    return html


def get_text_with_markdown_data(soup):

    for img in soup.find_all("img"):
        image_equation_tag = bs4.Tag(name="image-equation")
        image_equation_tag.string = "!!![image]({})!!!".format(img["src"])
        img.replace_with(image_equation_tag)

    str_soup = str(soup)
    # exchange <sub></sub>, <sup></sup> tags by markdowns
    str_soup = str_soup.replace("<sub>", SubscriptMarkDown.start)
    str_soup = str_soup.replace("</sub>", SubscriptMarkDown.end)
    str_soup = str_soup.replace("<sup>", SuperscriptMarkDown.start)
    str_soup = str_soup.replace("</sup>", SuperscriptMarkDown.end)
    # quoted = quote_mml(str_soup).encode("utf8")
    quoted = quote_mml(str_soup)
    soup = BeautifulSoup(quoted, "html.parser")
    text = soup.get_text(separator="\n")
    unquoted = unquote_mml(text)
    unquoted = unquoted.replace(
        '<span class="equation">', EquationMarkDown.start
    ).replace("</span>", EquationMarkDown.end)
    return unquoted
