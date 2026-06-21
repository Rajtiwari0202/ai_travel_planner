import { expect, test } from "@playwright/test";

test("creates a trip and renders the itinerary workspace", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /explainable agentic travel plans/i })).toBeVisible();
  await page.getByRole("button", { name: /create optimized itinerary/i }).click();
  await expect(page.getByText(/agent activity/i)).toBeVisible();
  await expect(page.getByRole("heading", { name: /goa itinerary/i })).toBeVisible({ timeout: 30_000 });
  await expect(page.getByText(/budget reconciliation/i)).toBeVisible();
  await expect(page.getByText(/coordinates come from the backend/i)).toBeVisible();
});
