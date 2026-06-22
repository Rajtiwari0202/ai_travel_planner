import { render, screen, within } from "@testing-library/react";
import { expect, test } from "vitest";
import { App } from "./App";

test("renders planner navigation", () => {
  render(<App />);
  expect(screen.getByText("TravelAgenticAI")).toBeInTheDocument();
  const navigation = screen.getByRole("navigation", { name: /primary/i });
  expect(within(navigation).getByRole("link", { name: /planner/i })).toBeInTheDocument();
  expect(within(navigation).getByRole("link", { name: /providers/i })).toBeInTheDocument();
  expect(within(navigation).getByRole("link", { name: /research/i })).toBeInTheDocument();
});
