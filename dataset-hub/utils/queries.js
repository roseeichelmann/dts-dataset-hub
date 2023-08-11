export const DATASETS_QUERY = {
  args: [
    { key: "limit", value: "500" },
    // {
    //   key: "order",
    //   value: "timestamp desc",
    // },
    {
      key: "select",
      value: "name",
    },
    // {
    //   key: "where",
    //   value: "device_type = 'camera'",
    // },
  ],
};
