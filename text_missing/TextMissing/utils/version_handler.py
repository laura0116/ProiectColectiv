from TextMissing.models import StatusChoices


class VersionHandler():
    @staticmethod
    def upgradeVersion(Document):
        version = Document.version
        whole, frac = version.split('.')
        frac = int(frac)
        whole = int(whole)
        if (Document.status == StatusChoices.DRAFT):
            if (whole > 0):
                whole = 0
                frac = 1
            else:
                frac += 1
        elif (Document.status == StatusChoices.FINAL):
            frac = 0
            if (whole < 1):
                whole = 1
            else:
                whole += 1
        elif (Document.status == StatusChoices.FINAL_REVISED):
            frac += 1
        version = str(whole) + '.' + str(frac)
        return version