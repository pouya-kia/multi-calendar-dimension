# Deploy Guide - نسخه 1.0.4

این راهنما برای publish کردن نسخه جدید پکیج به PyPI است.

## تغییرات در این نسخه (1.0.4)

✅ **Bug Fix**: رفع مشکل import کردن `DateRangeGenerator`
- قبلا: `ImportError: cannot import name 'DateRangeGenerator'`
- الان: کار می‌کنه ✓

## قبل از Deploy

### 1. بررسی تغییرات
```bash
cd ad_hoc/multi-calendar-dimension
git status
```

### 2. اطمینان از نصب ابزارهای لازم
```bash
pip install --upgrade build twine
```

## مراحل Deploy

### مرحله 1: پاک کردن build های قبلی
```bash
cd ad_hoc/multi-calendar-dimension
rm -rf dist/ build/ *.egg-info
```

یا در Windows PowerShell:
```powershell
cd "ad_hoc/multi-calendar-dimension"
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue
```

### مرحله 2: ساخت پکیج
```bash
python -m build
```

این دستور دو فایل می‌سازه:
- `dist/multi_calendar_dimension-1.0.4-py3-none-any.whl`
- `dist/multi_calendar_dimension-1.0.4.tar.gz`

### مرحله 3: بررسی پکیج
```bash
twine check dist/*
```

باید خروجی بگه: `PASSED`

### مرحله 4: تست در TestPyPI (اختیاری ولی توصیه می‌شه)
```bash
# آپلود به TestPyPI
twine upload --repository testpypi dist/*

# تست نصب از TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ multi-calendar-dimension==1.0.4
```

### مرحله 5: آپلود به PyPI اصلی
```bash
twine upload dist/*
```

این دستور از شما username و password (یا API token) PyPI رو می‌خواد.

**نکته**: بهتره از API Token استفاده کنی:
- برو به: https://pypi.org/manage/account/token/
- یک API token جدید بساز
- username: `__token__`
- password: `pypi-...` (توکنی که ساختی)

### مرحله 6: بررسی در PyPI
بعد از 1-2 دقیقه، برو به:
https://pypi.org/project/multi-calendar-dimension/

باید نسخه 1.0.4 رو ببینی!

### مرحله 7: تست نصب نهایی
```bash
# نصب از PyPI
pip install --upgrade multi-calendar-dimension

# تست
python -c "from multi_calendar_dimension import DateRangeGenerator; print('✓ Success!')"
```

## Git Commit & Tag

بعد از deploy موفق، تغییرات رو commit کن:

```bash
git add .
git commit -m "Release v1.0.4 - Fix DateRangeGenerator import error"
git tag -a v1.0.4 -m "Version 1.0.4 - Bug fix release"
git push origin main
git push origin v1.0.4
```

## عیب‌یابی

### مشکل: "Invalid distribution file"
**راه حل**: مطمئن شو که فایل `pyproject.toml` صحیح است و build دوباره کن

### مشکل: "Version already exists"
**راه حل**: نسخه قبلا آپلود شده. باید نسخه رو افزایش بدی (مثلا 1.0.5)

### مشکل: "403 Forbidden"
**راه حل**: 
- مطمئن شو که API token درست است
- مطمئن شو که دسترسی به پروژه داری

### مشکل: "Package name already taken"
**راه حل**: اگر اولین بار است، باید اول پروژه رو تو PyPI ثبت کنی

## فایل‌های تغییر کرده در این نسخه

- ✅ `pyproject.toml` - نسخه به 1.0.4 تغییر کرد
- ✅ `multi_calendar_dimension/__init__.py` - نسخه و import ها اصلاح شد
- ✅ `RELEASE_NOTES.md` - یادداشت‌های نسخه 1.0.4 اضافه شد

## چک‌لیست نهایی

- [ ] نسخه در `pyproject.toml` به 1.0.4 تغییر کرده
- [ ] نسخه در `__init__.py` به 1.0.4 تغییر کرده
- [ ] `RELEASE_NOTES.md` آپدیت شده
- [ ] تست‌ها پاس می‌شن
- [ ] پکیج build شده
- [ ] پکیج چک شده با twine
- [ ] آپلود به PyPI انجام شده
- [ ] نصب و تست نهایی OK
- [ ] Git commit و tag زده شده

---

## نکات مهم

1. **هیچ وقت نمی‌تونی یک نسخه رو دوباره آپلود کنی** - پس قبل از upload مطمئن شو همه چیز درسته
2. **از TestPyPI استفاده کن** - برای تست قبل از upload اصلی
3. **API Token امن‌تره** - به جای username/password
4. **همیشه Release Notes بنویس** - برای کاربران مهمه

## لینک‌های مفید

- PyPI Project: https://pypi.org/project/multi-calendar-dimension/
- TestPyPI: https://test.pypi.org/
- Twine Docs: https://twine.readthedocs.io/
- Python Packaging: https://packaging.python.org/

