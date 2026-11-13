export default function Panel({
  children,
  className = "",
  elevated = false,
  padding = true,
  as: Tag = "div",
  ...props
}) {
  return (
    <Tag
      className={[
        elevated ? "qk-panel-elevated" : "qk-panel",
        padding ? "p-4 sm:p-5" : "",
        className,
      ]
        .filter(Boolean)
        .join(" ")}
      {...props}
    >
      {children}
    </Tag>
  );
}
