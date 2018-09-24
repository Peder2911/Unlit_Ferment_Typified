# Downloads and places xpdf-tools in the right location.
# Run from Unlit_Ferment_Typified root

wget "https://xpdfreader-dl.s3.amazonaws.com/xpdf-tools-linux-4.00.tar.gz" &&
tar -xf "xpdf-tools-linux-4.00.tar.gz" -C lib/xpdf &&
rm "xpdf-tools-linux-4.00.tar.gz" &&
mv lib/xpdf/xpdf-tools-linux-4.00/bin64/* lib/xpdf &&
rm -r lib/xpdf/xpdf-tools-linux-4.00
