# Cinesis Good Fit Test

Completed solution for the Cinesis Good Fit Test assessment.

## Files

- `cinesis_good_fit_test_completed.xlsx` contains the completed workbook.
- `solution.py` contains the Python logic used for the load ranking section.

## Approach

The solution extracts the driver profile from the provided transcript and applies the stated constraints:

- Current location: Dallas TX
- Home base: San Antonio TX
- Minimum acceptable rate: $2.00 per mile
- Equipment: Hotshot plus Gooseneck plus Flatbed
- Maximum weight capacity: 14,000 lb

The script filters out incomplete loads and ineligible loads based on equipment and weight. It then calculates effective rate per mile using total route distance which includes deadhead from current location to origin plus loaded miles plus deadhead back to home base.

## Run

```bash
python solution.py
```

Expected output:

```text
1 L08 3.558
```

## Notes

Only one load met all constraints under the total route distance calculation. Loads with missing price or missing destination were rejected as incomplete. Loads that did not match equipment or exceeded the weight limit were rejected as ineligible.
