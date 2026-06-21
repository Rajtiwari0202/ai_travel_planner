import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import type { BudgetBreakdown, ScoreBreakdown } from "../../types/api";

const COLORS = ["#1f7a8c", "#2f6f4e", "#b85f45", "#8a7a3f", "#465a69", "#7d5a48", "#9b4d5c"];

export function BudgetPanel({ budget, score }: { budget: BudgetBreakdown; score: ScoreBreakdown }) {
  const rows = [
    ["Transport", budget.transport],
    ["Stay", budget.accommodation],
    ["Activities", budget.activities],
    ["Local", budget.local_transport],
    ["Food", budget.food],
    ["Fees", budget.taxes_and_fees],
    ["Contingency", budget.contingency],
  ];
  const data = rows.map(([name, value]) => ({ name, value: Number(value) }));
  return (
    <section className="rounded-lg border border-ink/10 bg-white p-4 shadow-soft" aria-label="Budget and score">
      <h2 className="font-semibold text-ink">Budget reconciliation</h2>
      <p className="mt-1 text-3xl font-semibold text-ink">
        {budget.currency} {budget.total.toLocaleString()}
      </p>
      <p className={budget.remaining >= 0 ? "text-sm font-medium text-leaf" : "text-sm font-medium text-clay"}>
        {budget.remaining >= 0 ? "Remaining" : "Over budget"} {budget.currency} {Math.abs(budget.remaining).toLocaleString()}
      </p>
      <div className="mt-4 h-48">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="name" innerRadius={48} outerRadius={72} paddingAngle={2}>
              {data.map((entry, index) => (
                <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value: number) => `${budget.currency} ${value.toLocaleString()}`} />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 grid gap-2 text-sm">
        {rows.map(([name, value]) => (
          <div key={name} className="flex justify-between border-b border-ink/10 pb-1">
            <span className="text-ink/65">{name}</span>
            <span className="font-semibold text-ink">
              {budget.currency} {Number(value).toLocaleString()}
            </span>
          </div>
        ))}
      </div>
      <div className="mt-4 rounded-md bg-paper p-3">
        <p className="text-sm font-semibold text-ink">Optimization score {(score.total_score * 100).toFixed(0)}%</p>
        <p className="mt-1 text-xs leading-5 text-ink/65">{score.explanation[0]}</p>
      </div>
    </section>
  );
}
