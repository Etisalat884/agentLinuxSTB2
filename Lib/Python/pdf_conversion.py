def convert_pdf(html_file_path):
    import asyncio
    import os
    from pyppeteer import launch

    pdf_file = html_file_path.replace(".html", "_expanded.pdf")

    async def _convert():
        browser = await launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ]
        )

        page = await browser.newPage()

        # ✅ Load file directly instead of HTTP
        html_url = f"file://{os.path.abspath(html_file_path)}"
        print("Opening URL:", html_url)

        await page.goto(html_url, {'waitUntil': 'networkidle2'})

        try:
            # ✅ Wait for Robot Framework main content
            await page.waitForSelector('#statistics', {'timeout': 15000})
            print("Page loaded successfully")
        except Exception:
            print("ERROR: Robot report did not load properly")
            await browser.close()
            return None

        # ✅ Ensure JS is fully loaded
        await page.waitForTimeout(5000)

        # ✅ Expand all sections safely
        print("Expanding all sections...")

        await page.evaluate("""
            async () => {
                function wait(ms) {
                    return new Promise(resolve => setTimeout(resolve, ms));
                }

                if (typeof expandAll === 'function') {
                    expandAll();
                    await wait(2000);
                }

                // Click all collapsed elements
                let elements = document.querySelectorAll('.collapsed');
                for (let el of elements) {
                    try {
                        el.click();
                        await wait(50);
                    } catch(e) {}
                }

                // Scroll to trigger lazy loading
                window.scrollTo(0, document.body.scrollHeight);
                await wait(2000);
                window.scrollTo(0, 0);
            }
        """)

        # ✅ Wait after expansion
        await page.waitForTimeout(10000)

        # ✅ Validate content before PDF
        content = await page.content()

        if "Test Statistics" not in content:
            print("ERROR: Not a valid Robot Framework report")
            with open("debug_failed.html", "w") as f:
                f.write(content)
            await browser.close()
            return None

        # ✅ Save debug HTML (optional but useful)
        with open("debug_success.html", "w") as f:
            f.write(content)

        print("Generating PDF...")

        # ✅ Generate real PDF
        await page.pdf({
            "path": pdf_file,
            "format": "A4",
            "printBackground": True,
            "margin": {
                "top": "10mm",
                "bottom": "10mm",
                "left": "10mm",
                "right": "10mm"
            }
        })

        await browser.close()

    # ✅ Run async properly
    asyncio.get_event_loop().run_until_complete(_convert())

    print("✅ PDF generated:", pdf_file)
    return pdf_file
