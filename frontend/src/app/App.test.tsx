import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";
import { App } from "./App";

test("renders planner navigation", () => {
  render(<App />);
  expect(screen.getByText("TravelAgenticAI")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: /create optimized itinerary/i })).toBeInTheDocument();
});
